from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    points: int
    rank: str
    donations_count: int
    
    class Config:
        from_attributes = True

class DonationCreate(BaseModel):
    user_id: int
    item_type: str
    location: str

class DonationResponse(BaseModel):
    id: int
    user_id: int
    item_type: str
    location: str
    timestamp: datetime
    points_awarded: int
    
    class Config:
        from_attributes = True

class NeedCreate(BaseModel):
    item_type: str
    urgency_level: str
    multiplier: float

class NeedResponse(BaseModel):
    id: int
    item_type: str
    urgency_level: str
    multiplier: float
    
    class Config:
        from_attributes = True

class DonateRequest(BaseModel):
    user_id: int
    item_type: str
    location: str

class DonateResponse(BaseModel):
    user_id: int
    points_awarded: int
    total_points: int
