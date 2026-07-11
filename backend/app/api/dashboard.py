"""Dashboard routes for BankShield AI"""

from typing import Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.models.alert import Alert
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/stats", response_model=Dict[str, Any])
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    # Get base query
    if current_user.is_admin:
        event_query = db.query(Event)
        alert_query = db.query(Alert)
    else:
        event_query = db.query(Event).filter(Event.user_id == current_user.id)
        alert_query = db.query(Alert).filter(Alert.user_id == current_user.id)
    
    # Count events by risk level
    total_events = event_query.count()
    critical_events = event_query.filter(Event.risk_level == "CRITICAL").count()
    high_events = event_query.filter(Event.risk_level == "HIGH").count()
    medium_events = event_query.filter(Event.risk_level == "MEDIUM").count()
    low_events = event_query.filter(Event.risk_level == "LOW").count()
    
    # Count alerts
    total_alerts = alert_query.count()
    critical_alerts = alert_query.filter(Alert.severity == "CRITICAL").count()
    high_alerts = alert_query.filter(Alert.severity == "HIGH").count()
    medium_alerts = alert_query.filter(Alert.severity == "MEDIUM").count()
    low_alerts = alert_query.filter(Alert.severity == "LOW").count()
    
    # Open alerts
    open_alerts = alert_query.filter(Alert.status == "OPEN").count()
    
    # Average risk score
    avg_risk = db.query(func.avg(Event.risk_score)).select_from(Event).scalar() or 0.0
    
    # Flagged events
    flagged_events = event_query.filter(Event.is_flagged == True).count()
    
    # Last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    events_24h = event_query.filter(Event.timestamp >= last_24h).count()
    alerts_24h = alert_query.filter(Alert.created_at >= last_24h).count()
    
    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "flagged_events": flagged_events,
        "average_risk_score": round(avg_risk, 2),
        "events_by_risk_level": {
            "CRITICAL": critical_events,
            "HIGH": high_events,
            "MEDIUM": medium_events,
            "LOW": low_events
        },
        "alerts_by_severity": {
            "CRITICAL": critical_alerts,
            "HIGH": high_alerts,
            "MEDIUM": medium_alerts,
            "LOW": low_alerts
        },
        "last_24_hours": {
            "events": events_24h,
            "alerts": alerts_24h
        }
    }

@router.get("/timeline")
def get_threat_timeline(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    hours: int = 24
):
    """Get threat timeline for last N hours"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    if current_user.is_admin:
        events = db.query(Event).filter(Event.timestamp >= start_time).order_by(Event.timestamp).all()
    else:
        events = db.query(Event).filter(
            (Event.user_id == current_user.id) & (Event.timestamp >= start_time)
        ).order_by(Event.timestamp).all()
    
    timeline_data = []
    for event in events:
        timeline_data.append({
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "risk_score": event.risk_score,
            "risk_level": event.risk_level,
            "user_id": event.user_id
        })
    
    return timeline_data

@router.get("/top-suspicious-users")
def get_top_suspicious_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get top suspicious users by average risk score"""
    if not current_user.is_admin:
        return [{"user_id": current_user.id, "avg_risk_score": current_user.risk_score}]
    
    query = db.query(
        Event.user_id,
        func.avg(Event.risk_score).label("avg_risk_score"),
        func.count(Event.id).label("event_count")
    ).group_by(Event.user_id).order_by(func.avg(Event.risk_score).desc()).limit(limit)
    
    results = query.all()
    
    return [
        {
            "user_id": r[0],
            "avg_risk_score": round(r[1], 2),
            "event_count": r[2]
        }
        for r in results
    ]

@router.get("/risk-distribution")
def get_risk_distribution(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk distribution pie chart data"""
    if current_user.is_admin:
        query = db.query(Event)
    else:
        query = db.query(Event).filter(Event.user_id == current_user.id)
    
    total = query.count()
    
    if total == 0:
        return {"labels": [], "data": []}
    
    critical = query.filter(Event.risk_level == "CRITICAL").count()
    high = query.filter(Event.risk_level == "HIGH").count()
    medium = query.filter(Event.risk_level == "MEDIUM").count()
    low = query.filter(Event.risk_level == "LOW").count()
    safe = query.filter(Event.risk_level == "SAFE").count()
    
    return {
        "labels": ["Critical", "High", "Medium", "Low", "Safe"],
        "data": [critical, high, medium, low, safe],
        "colors": ["#FF3333", "#FF9933", "#FFD700", "#90EE90", "#00AA00"]
    }
