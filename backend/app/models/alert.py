"""Alert model for BankShield AI"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True, index=True)
    
    # Alert details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, nullable=False, index=True)  # CRITICAL, HIGH, MEDIUM, LOW
    alert_type = Column(String, nullable=False)  # fraud, anomaly, policy_violation, etc.
    
    # Status
    status = Column(String, default="OPEN", index=True)  # OPEN, ACKNOWLEDGED, RESOLVED, FALSE_POSITIVE
    is_active = Column(Boolean, default=True)
    
    # Details
    risk_score = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.0)
    threat_indicators = Column(String, nullable=True)  # Comma-separated indicators
    recommended_action = Column(String, nullable=True)
    
    # Timeline
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="alerts")
    event = relationship("Event", back_populates="alerts")
    
    def __repr__(self):
        return f"<Alert(id={self.id}, severity={self.severity}, status={self.status})>"
