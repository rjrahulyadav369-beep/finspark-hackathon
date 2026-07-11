"""Alert schemas for BankShield AI"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class AlertBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    alert_type: str

class AlertCreate(AlertBase):
    user_id: int
    event_id: Optional[int] = None
    risk_score: float = 0.0
    confidence_score: float = 0.0
    threat_indicators: Optional[str] = None
    recommended_action: Optional[str] = None

class AlertResponse(AlertBase):
    id: int
    user_id: int
    event_id: Optional[int]
    status: str
    is_active: bool
    risk_score: float
    confidence_score: float
    threat_indicators: Optional[str]
    recommended_action: Optional[str]
    created_at: datetime
    updated_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None
