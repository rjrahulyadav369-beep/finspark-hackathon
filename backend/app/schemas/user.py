"""User schemas for BankShield AI"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    risk_score: float
    threat_level: str
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserWithEvents(UserResponse):
    events: Optional[List] = []
