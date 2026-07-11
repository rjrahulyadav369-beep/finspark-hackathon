"""Prediction routes for BankShield AI"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.schemas.event import EventCreate
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.api.auth import get_current_user
from app.services.ml_service import predict_risk, get_ml_model

router = APIRouter()

@router.post("/event", response_model=Dict[str, Any])
def predict_event_risk(
    event: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict risk for an event"""
    # Verify authorization
    if event.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Create event in database
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Get prediction
    db_event = predict_risk(db_event, db)
    db.commit()
    
    return {
        "event_id": db_event.id,
        "risk_score": db_event.risk_score,
        "risk_level": db_event.risk_level,
        "confidence_score": db_event.confidence_score,
        "threat_category": db_event.threat_category,
        "explanation": db_event.explanation,
        "recommended_action": db_event.recommended_action,
        "is_flagged": db_event.is_flagged
    }

@router.post("/batch", response_model=list)
def predict_batch(
    events: list[EventCreate],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict risk for multiple events"""
    results = []
    
    for event in events:
        # Verify authorization
        if event.user_id != current_user.id and not current_user.is_admin:
            continue
        
        # Create event
        db_event = Event(**event.dict())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
        # Predict
        db_event = predict_risk(db_event, db)
        db.commit()
        
        results.append({
            "event_id": db_event.id,
            "risk_score": db_event.risk_score,
            "risk_level": db_event.risk_level,
            "confidence_score": db_event.confidence_score
        })
    
    return results

@router.get("/model/info")
def get_model_info():
    """Get information about the ML model"""
    model_info = get_ml_model()
    
    return {
        "model_type": model_info.get("model_type", "Random Forest"),
        "version": model_info.get("version", "1.0.0"),
        "accuracy": model_info.get("accuracy"),
        "precision": model_info.get("precision"),
        "recall": model_info.get("recall"),
        "f1_score": model_info.get("f1_score"),
        "features": model_info.get("features", [])
    }
