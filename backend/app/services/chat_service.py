"""Chat service for BankShield AI"""

from typing import List
from app.models.event import Event

def generate_response(query: str, events: List[Event], user_id: int) -> str:
    """Generate AI response for user query"""
    
    query_lower = query.lower()
    
    # Analyze events
    if not events:
        return "No events found for this user."
    
    # Answer: Why was account flagged?
    if "why" in query_lower and "flag" in query_lower:
        flagged_events = [e for e in events if e.is_flagged]
        if flagged_events:
            reasons = []
            for e in flagged_events[:3]:
                if e.explanation:
                    reasons.append(e.explanation)
            return f"The account was flagged due to: {'; '.join(reasons) if reasons else 'Suspicious activity detected'}"
        return "No flagged events found."
    
    # Answer: What are recent activities?
    if "recent" in query_lower or "activity" in query_lower:
        recent = events[:5]
        activities = []
        for e in recent:
            activities.append(f"{e.event_type.upper()} - Risk: {e.risk_level} ({e.risk_score})")
        return f"Recent activities: {'; '.join(activities)}"
    
    # Answer: Is account secure?
    if "secure" in query_lower or "safe" in query_lower:
        high_risk = sum(1 for e in events if e.risk_level in ["HIGH", "CRITICAL"])
        total = len(events)
        if high_risk > total * 0.3:
            return f"⚠️ Account shows {high_risk} high-risk events out of {total} total events. Recommend immediate security review."
        return f"✅ Account appears secure. {high_risk} high-risk events detected out of {total}."
    
    # Answer: Transaction history?
    if "transaction" in query_lower:
        transactions = [e for e in events if e.event_type == "transaction"]
        if transactions:
            total_amount = sum(e.transaction_amount for e in transactions)
            return f"Found {len(transactions)} transactions totaling {total_amount}. Average transaction: {total_amount/len(transactions):.2f}"
        return "No transactions found."
    
    # Answer: Device information?
    if "device" in query_lower:
        devices = set(e.device_name for e in events if e.device_name)
        return f"Found {len(devices)} devices: {', '.join(devices) if devices else 'No device information'}"
    
    # Answer: Location information?
    if "location" in query_lower:
        locations = set(e.location for e in events if e.location)
        return f"Found {len(locations)} locations: {', '.join(locations) if locations else 'No location information'}"
    
    # Answer: Failed logins?
    if "login" in query_lower and "fail" in query_lower:
        failed = [e for e in events if e.event_type == "failed_login"]
        return f"Found {len(failed)} failed login attempts."
    
    # Default response
    avg_risk = sum(e.risk_score for e in events) / len(events)
    return f"User has {len(events)} total events with average risk score of {avg_risk:.2f}. Provide more specific queries for detailed analysis."
