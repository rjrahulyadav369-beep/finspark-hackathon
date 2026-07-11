"""Event schemas for BankShield AI"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class EventBase(BaseModel):
    event_type: str
    transaction_amount: float = 0.0
    transaction_type: Optional[str] = None
    device_id: Optional[str] = None
    device_name: Optional[str] = None
    location: Optional[str] = None
    ip_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    otp_attempts: int = 0
    failed_login_attempts: int = 0

class EventCreate(EventBase):
    user_id: int

class EventResponse(EventBase):
    id: int
    user_id: int
    timestamp: datetime
    risk_score: float
    risk_level: str
    confidence_score: float
    threat_category: Optional[str]
    is_flagged: bool
    explanation: Optional[str]
    recommended_action: Optional[str]
    processed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EventFilter(BaseModel):
    user_id: Optional[int] = None
    event_type: Optional[str] = None
    risk_level: Optional[str] = None
    is_flagged: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
    offset: int = 0
