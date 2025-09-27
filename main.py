from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, User, Donation, Need, engine
from schemas import (
    DonateRequest, DonateResponse, UserCreate, UserResponse,
    DonationResponse, NeedCreate, NeedResponse
)
from typing import List
import math

app = FastAPI(title="Donation Platform API", version="1.0.0")

# Health check endpoint
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# User endpoints
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Need endpoints
@app.post("/needs/", response_model=NeedResponse)
def create_need(need: NeedCreate, db: Session = Depends(get_db)):
    db_need = Need(
        item_type=need.item_type,
        urgency_level=need.urgency_level,
        multiplier=need.multiplier
    )
    db.add(db_need)
    db.commit()
    db.refresh(db_need)
    return db_need

@app.get("/needs/", response_model=List[NeedResponse])
def get_needs(db: Session = Depends(get_db)):
    needs = db.query(Need).all()
    return needs

def calculate_rank(points: int) -> str:
    """Calculate user rank based on total points"""
    if points >= 10000:
        return "Diamond"
    elif points >= 5000:
        return "Platinum"
    elif points >= 2000:
        return "Gold"
    elif points >= 500:
        return "Silver"
    else:
        return "Bronze"

def calculate_frequency_bonus(donations_count: int) -> float:
    """Calculate frequency bonus multiplier based on donation count"""
    if donations_count >= 50:
        return 2.0
    elif donations_count >= 20:
        return 1.5
    elif donations_count >= 10:
        return 1.2
    elif donations_count >= 5:
        return 1.1
    else:
        return 1.0

@app.post("/donate", response_model=DonateResponse)
def donate(request: DonateRequest, db: Session = Depends(get_db)):
    # Validate user exists
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate base points
    base_points = 100
    
    # Check if item matches any current needs for urgency multiplier
    need = db.query(Need).filter(Need.item_type == request.item_type).first()
    urgency_multiplier = need.multiplier if need else 1.0
    
    # Calculate frequency bonus based on current donation count
    frequency_bonus = calculate_frequency_bonus(user.donations_count)
    
    # Calculate total points awarded
    points_awarded = int(base_points * urgency_multiplier * frequency_bonus)
    
    # Create donation record
    donation = Donation(
        user_id=request.user_id,
        item_type=request.item_type,
        location=request.location,
        points_awarded=points_awarded
    )
    db.add(donation)
    
    # Update user stats
    user.points += points_awarded
    user.donations_count += 1
    user.rank = calculate_rank(user.points)
    
    db.commit()
    db.refresh(user)
    
    return DonateResponse(
        user_id=user.id,
        points_awarded=points_awarded,
        total_points=user.points
    )

@app.get("/donations/", response_model=List[DonationResponse])
def get_donations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    donations = db.query(Donation).offset(skip).limit(limit).all()
    return donations

@app.get("/donations/user/{user_id}", response_model=List[DonationResponse])
def get_user_donations(user_id: int, db: Session = Depends(get_db)):
    donations = db.query(Donation).filter(Donation.user_id == user_id).all()
    return donations

# Initialize some sample needs data
@app.on_event("startup")
async def startup_event():
    from database import SessionLocal
    db = SessionLocal()
    
    # Check if needs already exist
    if db.query(Need).count() == 0:
        sample_needs = [
            Need(item_type="food", urgency_level="high", multiplier=1.5),
            Need(item_type="clothing", urgency_level="medium", multiplier=1.2),
            Need(item_type="toys", urgency_level="low", multiplier=1.0),
            Need(item_type="medical_supplies", urgency_level="critical", multiplier=2.0),
            Need(item_type="books", urgency_level="medium", multiplier=1.1),
            Need(item_type="electronics", urgency_level="low", multiplier=1.0),
        ]
        
        for need in sample_needs:
            db.add(need)
        db.commit()
    
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
