"""Prediction schemas for BankShield AI"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    user_id: int
    event_data: Dict[str, Any]
    model_name: str = "random_forest"

class PredictionResponse(BaseModel):
    id: int
    user_id: int
    model_name: str
    model_version: str
    predicted_class: str
    predicted_probability: float
    confidence_score: float
    top_features: Optional[List[Dict]] = None
    feature_importance: Optional[Dict] = None
    accuracy: Optional[float]
    precision: Optional[float]
    recall: Optional[float]
    f1_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True
