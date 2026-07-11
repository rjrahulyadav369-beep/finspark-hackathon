"""Reports routes for BankShield AI"""

from typing import Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.models.alert import Alert
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/summary")
def get_report_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = 30
):
    """Get summary report for last N days"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    if current_user.is_admin:
        event_query = db.query(Event).filter(Event.created_at >= start_date)
        alert_query = db.query(Alert).filter(Alert.created_at >= start_date)
    else:
        event_query = db.query(Event).filter(
            (Event.user_id == current_user.id) & (Event.created_at >= start_date)
        )
        alert_query = db.query(Alert).filter(
            (Alert.user_id == current_user.id) & (Alert.created_at >= start_date)
        )
    
    events = event_query.all()
    alerts = alert_query.all()
    
    return {
        "period_days": days,
        "report_date": datetime.utcnow(),
        "total_events": len(events),
        "total_alerts": len(alerts),
        "critical_events": sum(1 for e in events if e.risk_level == "CRITICAL"),
        "high_events": sum(1 for e in events if e.risk_level == "HIGH"),
        "avg_risk_score": round(sum(e.risk_score for e in events) / len(events), 2) if events else 0,
        "top_threat_categories": get_top_threat_categories(events),
        "top_event_types": get_top_event_types(events)
    }

@router.get("/export-csv")
def export_events_csv(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = 30
):
    """Export events to CSV"""
    import csv
    import tempfile
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    if current_user.is_admin:
        events = db.query(Event).filter(Event.created_at >= start_date).all()
    else:
        events = db.query(Event).filter(
            (Event.user_id == current_user.id) & (Event.created_at >= start_date)
        ).all()
    
    # Create CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "User ID", "Timestamp", "Event Type", "Amount",
            "Device", "Location", "IP", "Risk Score", "Risk Level", "Is Flagged"
        ])
        
        for event in events:
            writer.writerow([
                event.id,
                event.user_id,
                event.timestamp,
                event.event_type,
                event.transaction_amount,
                event.device_name,
                event.location,
                event.ip_address,
                event.risk_score,
                event.risk_level,
                event.is_flagged
            ])
        
        return FileResponse(
            f.name,
            media_type="text/csv",
            filename=f"events_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        )

def get_top_threat_categories(events):
    """Get top threat categories"""
    categories = {}
    for event in events:
        if event.threat_category:
            categories[event.threat_category] = categories.get(event.threat_category, 0) + 1
    return sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]

def get_top_event_types(events):
    """Get top event types"""
    types = {}
    for event in events:
        types[event.event_type] = types.get(event.event_type, 0) + 1
    return sorted(types.items(), key=lambda x: x[1], reverse=True)[:5]
