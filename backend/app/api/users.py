"""User routes for BankShield AI"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.schemas.user import UserResponse
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile"""
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/{user_id}/risk-profile")
def get_user_risk_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user risk profile"""
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's events
    events = db.query(Event).filter(Event.user_id == user_id).all()
    
    if not events:
        return {
            "user_id": user_id,
            "overall_risk_score": 0.0,
            "threat_level": "SAFE",
            "total_events": 0,
            "flagged_events": 0,
            "avg_risk_score": 0.0
        }
    
    flagged = sum(1 for e in events if e.is_flagged)
    avg_risk = sum(e.risk_score for e in events) / len(events)
    
    return {
        "user_id": user_id,
        "overall_risk_score": user.risk_score,
        "threat_level": user.threat_level,
        "total_events": len(events),
        "flagged_events": flagged,
        "avg_risk_score": round(avg_risk, 2)
    }

@router.get("/{user_id}/transaction-history")
def get_user_transaction_history(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get user transaction history"""
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    transactions = db.query(Event).filter(
        (Event.user_id == user_id) & (Event.event_type == "transaction")
    ).order_by(Event.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "id": t.id,
            "timestamp": t.timestamp,
            "amount": t.transaction_amount,
            "type": t.transaction_type,
            "location": t.location,
            "risk_score": t.risk_score
        }
        for t in transactions
    ]

@router.get("/{user_id}/login-history")
def get_user_login_history(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get user login history"""
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    logins = db.query(Event).filter(
        (Event.user_id == user_id) & (Event.event_type.in_(["login", "failed_login"]))
    ).order_by(Event.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "id": l.id,
            "timestamp": l.timestamp,
            "event_type": l.event_type,
            "device": l.device_name,
            "location": l.location,
            "ip_address": l.ip_address,
            "risk_score": l.risk_score
        }
        for l in logins
    ]

@router.get("/{user_id}/devices")
def get_user_devices(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's known devices"""
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    events = db.query(Event).filter(Event.user_id == user_id).all()
    
    # Extract unique devices
    devices = {}
    for event in events:
        if event.device_id and event.device_name:
            devices[event.device_id] = {
                "device_id": event.device_id,
                "device_name": event.device_name,
                "last_seen": event.timestamp,
                "location": event.location
            }
    
    return list(devices.values())
