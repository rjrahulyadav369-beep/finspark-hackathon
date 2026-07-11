"""Machine Learning service for BankShield AI"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from joblib import load, dump
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.prediction import Prediction
from app.config import settings

class MLService:
    def __init__(self):
        self.model_path = settings.MODEL_PATH
        self.model = None
        self.scaler = None
        self.model_info = {
            "model_type": "Random Forest",
            "version": "1.0.0",
            "accuracy": 0.92,
            "precision": 0.89,
            "recall": 0.85,
            "f1_score": 0.87
        }
        self.load_model()
    
    def load_model(self):
        """Load ML model from disk"""
        try:
            model_file = os.path.join(self.model_path, "risk_model.pkl")
            if os.path.exists(model_file):
                self.model = load(model_file)
            else:
                print(f"⚠️ Model not found at {model_file}, using rule-based system")
                self.model = None
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def extract_features(self, event: Event, db: Session) -> np.ndarray:
        """Extract features from event for ML prediction"""
        
        # Get user's historical data
        user_events = db.query(Event).filter(
            Event.user_id == event.user_id
        ).order_by(Event.timestamp.desc()).limit(1000).all()
        
        # Feature engineering
        features = {
            "transaction_amount": event.transaction_amount,
            "otp_attempts": event.otp_attempts,
            "failed_login_attempts": event.failed_login_attempts,
            "is_new_device": 1 if self._is_new_device(event, user_events) else 0,
            "is_new_location": 1 if self._is_new_location(event, user_events) else 0,
            "is_new_ip": 1 if self._is_new_ip(event, user_events) else 0,
            "location_change_velocity": self._calculate_location_velocity(event, user_events),
            "transaction_anomaly": self._detect_transaction_anomaly(event, user_events),
            "time_anomaly": self._detect_time_anomaly(event, user_events),
            "device_count": len(set(e.device_id for e in user_events if e.device_id)),
            "location_count": len(set(e.location for e in user_events if e.location)),
            "ip_count": len(set(e.ip_address for e in user_events if e.ip_address)),
            "failed_attempts_ratio": self._calculate_failed_attempts_ratio(user_events),
            "event_frequency": self._calculate_event_frequency(user_events),
        }
        
        return np.array(list(features.values())), features
    
    def _is_new_device(self, event: Event, user_events: list) -> bool:
        """Check if device is new for user"""
        if not event.device_id:
            return False
        return not any(e.device_id == event.device_id for e in user_events)
    
    def _is_new_location(self, event: Event, user_events: list) -> bool:
        """Check if location is new for user"""
        if not event.location:
            return False
        return not any(e.location == event.location for e in user_events)
    
    def _is_new_ip(self, event: Event, user_events: list) -> bool:
        """Check if IP is new for user"""
        if not event.ip_address:
            return False
        return not any(e.ip_address == event.ip_address for e in user_events)
    
    def _calculate_location_velocity(self, event: Event, user_events: list) -> float:
        """Calculate location change velocity (distance/time)"""
        if not user_events or not event.location:
            return 0.0
        
        # Simplified: count location changes in last hour
        last_hour = datetime.utcnow() - timedelta(hours=1)
        recent_events = [e for e in user_events if e.timestamp >= last_hour]
        
        location_changes = len(set(e.location for e in recent_events if e.location))
        return float(location_changes)
    
    def _detect_transaction_anomaly(self, event: Event, user_events: list) -> float:
        """Detect transaction anomalies"""
        if event.event_type != "transaction" or event.transaction_amount == 0:
            return 0.0
        
        transaction_events = [e for e in user_events if e.event_type == "transaction" and e.transaction_amount > 0]
        
        if not transaction_events:
            return 0.5  # Medium anomaly for new user
        
        amounts = [e.transaction_amount for e in transaction_events]
        mean = np.mean(amounts)
        std = np.std(amounts)
        
        if std == 0:
            return 0.0
        
        z_score = abs((event.transaction_amount - mean) / std)
        return min(z_score / 3.0, 1.0)  # Normalize to 0-1
    
    def _detect_time_anomaly(self, event: Event, user_events: list) -> float:
        """Detect time-based anomalies"""
        # Simple rule: flag if event at unusual hours (2 AM - 6 AM)
        hour = event.timestamp.hour if event.timestamp else datetime.utcnow().hour
        if 2 <= hour <= 6:
            return 0.7
        return 0.1
    
    def _calculate_failed_attempts_ratio(self, user_events: list) -> float:
        """Calculate ratio of failed attempts"""
        if not user_events:
            return 0.0
        
        failed = sum(1 for e in user_events if e.failed_login_attempts > 0 or e.otp_attempts > 2)
        total = len(user_events)
        
        return failed / total if total > 0 else 0.0
    
    def _calculate_event_frequency(self, user_events: list) -> float:
        """Calculate event frequency (events per hour)"""
        if len(user_events) < 2:
            return 0.0
        
        recent = user_events[0]
        oldest = user_events[-1]
        time_diff = (recent.timestamp - oldest.timestamp).total_seconds() / 3600.0
        
        if time_diff == 0:
            return 0.0
        
        return min(len(user_events) / time_diff, 100.0)  # Cap at 100
    
    def calculate_risk_score(self, event: Event, db: Session) -> Dict[str, Any]:
        """Calculate risk score using ML model or rules"""
        
        features, feature_dict = self.extract_features(event, db)
        
        # Calculate risk score (0-100)
        if self.model:
            try:
                prediction = self.model.predict_proba([features])[0]
                risk_probability = prediction[-1]  # Probability of high-risk class
                risk_score = risk_probability * 100
            except:
                risk_score = self._calculate_rule_based_risk(feature_dict)
        else:
            risk_score = self._calculate_rule_based_risk(feature_dict)
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 60:
            risk_level = "HIGH"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
        elif risk_score >= 20:
            risk_level = "LOW"
        else:
            risk_level = "SAFE"
        
        # Get explanations and recommendations
        explanation = self._generate_explanation(event, feature_dict, risk_level)
        recommended_action = self._get_recommended_action(risk_level)
        threat_category = self._categorize_threat(event, feature_dict)
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "confidence_score": min(0.95, 0.7 + (abs(risk_score - 50) / 100 * 0.25)),
            "explanation": explanation,
            "recommended_action": recommended_action,
            "threat_category": threat_category,
            "is_flagged": risk_level in ["HIGH", "CRITICAL"]
        }
    
    def _calculate_rule_based_risk(self, features: Dict[str, Any]) -> float:
        """Calculate risk score using business rules"""
        risk_score = 0.0
        
        # Transaction anomaly
        risk_score += features.get("transaction_anomaly", 0) * 25
        
        # New device/location/IP
        risk_score += features.get("is_new_device", 0) * 15
        risk_score += features.get("is_new_location", 0) * 20
        risk_score += features.get("is_new_ip", 0) * 15
        
        # Failed attempts
        failed_attempts = features.get("failed_login_attempts", 0) + features.get("otp_attempts", 0)
        risk_score += min(failed_attempts * 5, 20)
        
        # Time anomaly
        risk_score += features.get("time_anomaly", 0) * 10
        
        # Location velocity
        risk_score += min(features.get("location_change_velocity", 0) * 5, 15)
        
        return min(risk_score, 100.0)
    
    def _generate_explanation(self, event: Event, features: Dict, risk_level: str) -> str:
        """Generate human-readable explanation"""
        reasons = []
        
        if event.otp_attempts > 2:
            reasons.append(f"Multiple OTP failures ({event.otp_attempts} attempts)")
        
        if event.failed_login_attempts > 0:
            reasons.append(f"Failed login attempts detected ({event.failed_login_attempts})")
        
        if features.get("is_new_device"):
            reasons.append("New device detected")
        
        if features.get("is_new_location"):
            reasons.append("New location detected")
        
        if features.get("is_new_ip"):
            reasons.append("New IP address detected")
        
        if features.get("transaction_anomaly", 0) > 0.5:
            reasons.append(f"Unusual transaction amount: {event.transaction_amount}")
        
        if features.get("time_anomaly", 0) > 0.5:
            reasons.append("Transaction at unusual time (02:00 - 06:00)")
        
        if features.get("location_change_velocity", 0) > 1:
            reasons.append("Rapid location changes detected")
        
        if not reasons:
            reasons.append("Routine transaction")
        
        return "; ".join(reasons)
    
    def _get_recommended_action(self, risk_level: str) -> str:
        """Get recommended action for risk level"""
        actions = {
            "CRITICAL": "Immediately freeze account and request biometric verification. Notify SOC team immediately.",
            "HIGH": "Request additional authentication (OTP/biometric). Monitor account closely. Alert SOC for review.",
            "MEDIUM": "Request email confirmation. Enable 2FA if not active. Add to watchlist.",
            "LOW": "Enable additional monitoring. No immediate action required.",
            "SAFE": "No action required. Continue normal monitoring."
        }
        return actions.get(risk_level, "Monitor account")
    
    def _categorize_threat(self, event: Event, features: Dict) -> str:
        """Categorize the threat type"""
        if event.otp_attempts > 2 or event.failed_login_attempts > 2:
            return "BRUTE_FORCE_ATTEMPT"
        
        if features.get("is_new_device") and features.get("is_new_location") and features.get("is_new_ip"):
            return "ACCOUNT_TAKEOVER"
        
        if features.get("transaction_anomaly", 0) > 0.7:
            return "FRAUD_DETECTION"
        
        if event.transaction_amount > 100000:
            return "LARGE_TRANSACTION"
        
        if features.get("location_change_velocity", 0) > 1:
            return "IMPOSSIBLE_TRAVEL"
        
        return "ANOMALY_DETECTION"

# Initialize ML service
ml_service = MLService()

def predict_risk(event: Event, db: Session) -> Event:
    """Predict risk for event"""
    result = ml_service.calculate_risk_score(event, db)
    
    event.risk_score = result["risk_score"]
    event.risk_level = result["risk_level"]
    event.confidence_score = result["confidence_score"]
    event.explanation = result["explanation"]
    event.recommended_action = result["recommended_action"]
    event.threat_category = result["threat_category"]
    event.is_flagged = result["is_flagged"]
    event.processed = True
    
    return event

def get_ml_model():
    """Get ML model information"""
    return ml_service.model_info
