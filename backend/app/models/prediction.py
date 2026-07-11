"""Prediction model for BankShield AI"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True, index=True)
    
    # Prediction details
    model_name = Column(String, nullable=False)  # random_forest, isolation_forest, xgboost
    model_version = Column(String, nullable=False)
    
    # Input features (stored as JSON)
    input_features = Column(JSON, nullable=True)
    
    # Predictions
    predicted_class = Column(String, nullable=False)  # SAFE, LOW, MEDIUM, HIGH, CRITICAL
    predicted_probability = Column(Float, nullable=False)  # 0.0 - 1.0
    confidence_score = Column(Float, nullable=False)
    
    # Feature importance
    top_features = Column(JSON, nullable=True)  # Top contributing features
    feature_importance = Column(JSON, nullable=True)  # Feature importance scores
    
    # Model metrics
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    
    # Timeline
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    event = relationship("Event", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, model={self.model_name}, class={self.predicted_class})>"
