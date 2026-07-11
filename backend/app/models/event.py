"""Event model for BankShield AI"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Event details
    event_type = Column(String, nullable=False, index=True)  # login, transaction, otp_failure, etc.
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Transaction details
    transaction_amount = Column(Float, default=0.0)
    transaction_type = Column(String, nullable=True)  # debit, credit, atm, transfer
    beneficiary = Column(String, nullable=True)
    
    # Device & Location
    device_id = Column(String, nullable=True, index=True)
    device_name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    ip_address = Column(String, nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Authentication
    otp_attempts = Column(Integer, default=0)
    failed_login_attempts = Column(Integer, default=0)
    
    # Risk assessment
    risk_score = Column(Float, default=0.0, index=True)
    risk_level = Column(String, default="SAFE")  # SAFE, LOW, MEDIUM, HIGH, CRITICAL
    confidence_score = Column(Float, default=0.0)
    threat_category = Column(String, nullable=True)
    is_flagged = Column(Boolean, default=False, index=True)
    
    # Explanation & Action
    explanation = Column(String, nullable=True)
    recommended_action = Column(String, nullable=True)
    additional_data = Column(JSON, nullable=True)  # Store extra data as JSON
    
    # Processing
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="events")
    alerts = relationship("Alert", back_populates="event", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Event(id={self.id}, user_id={self.user_id}, event_type={self.event_type}, risk_score={self.risk_score})>"
