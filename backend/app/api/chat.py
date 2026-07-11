"""Chat AI routes for BankShield AI"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.api.auth import get_current_user
from app.services.chat_service import generate_response

router = APIRouter()

class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

@router.post("/ask")
def chat_with_ai(
    query: str,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI about user account"""
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Get user's events
    events = db.query(Event).filter(Event.user_id == user_id).order_by(Event.timestamp.desc()).limit(100).all()
    
    if not events:
        return {
            "response": "No events found for this user.",
            "confidence": 1.0
        }
    
    # Generate AI response
    response = generate_response(query, events, user_id)
    
    return {
        "query": query,
        "response": response,
        "timestamp": datetime.utcnow(),
        "events_analyzed": len(events)
    }

@router.post("/explain-alert")
def explain_alert(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI explanation for flagged event"""
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
            detail="Not authorized"
        )
    
    return {
        "event_id": event_id,
        "risk_score": event.risk_score,
        "risk_level": event.risk_level,
        "explanation": event.explanation,
        "recommended_action": event.recommended_action,
        "threat_category": event.threat_category,
        "confidence_score": event.confidence_score
    }

from datetime import datetime
