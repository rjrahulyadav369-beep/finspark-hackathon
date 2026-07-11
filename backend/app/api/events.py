"""Event routes for BankShield AI"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse, EventFilter
from app.api.auth import get_current_user
from app.services.ml_service import predict_risk

router = APIRouter()

@router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new security event"""
    # Verify user owns this event
    if event.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create event for this user"
        )
    
    # Create event
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    
    # Get ML prediction
    db.refresh(db_event)
    db_event = predict_risk(db_event, db)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.get("/", response_model=List[EventResponse])
def get_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    user_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    is_flagged: Optional[bool] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get filtered events"""
    query = db.query(Event)
    
    # Admin can see all, others only their own
    if not current_user.is_admin:
        query = query.filter(Event.user_id == current_user.id)
    elif user_id:
        query = query.filter(Event.user_id == user_id)
    
    # Apply filters
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if risk_level:
        query = query.filter(Event.risk_level == risk_level)
    if is_flagged is not None:
        query = query.filter(Event.is_flagged == is_flagged)
    if start_date:
        query = query.filter(Event.timestamp >= start_date)
    if end_date:
        query = query.filter(Event.timestamp <= end_date)
    
    # Pagination
    events = query.order_by(Event.timestamp.desc()).offset(offset).limit(limit).all()
    return events

@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check authorization
    if event.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this event"
        )
    
    return event

@router.get("/user/{user_id}", response_model=List[EventResponse])
def get_user_events(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, le=500),
    offset: int = Query(0, ge=0)
):
    """Get events for specific user"""
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these events"
        )
    
    events = db.query(Event).filter(
        Event.user_id == user_id
    ).order_by(
        Event.timestamp.desc()
    ).offset(offset).limit(limit).all()
    
    return events
