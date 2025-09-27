from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from database import get_db, User, Donation, Need, engine
from schemas import (
    DonateRequest, DonateResponse, UserCreate, UserResponse,
    DonationResponse, NeedCreate, NeedResponse, LeaderboardEntry
)
from typing import List
import math
import json

# Initialize some sample needs data
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
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
    yield
    # Shutdown (if needed)

app = FastAPI(title="Donation Platform API", version="1.0.0", lifespan=lifespan)

# Health check endpoint
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# User endpoints
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, badges="")  # Initialize badges as empty string
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Convert badges JSON to list for response
    response_user = UserResponse(
        id=db_user.id,
        name=db_user.name,
        points=db_user.points,
        rank=db_user.rank,
        donations_count=db_user.donations_count,
        badges=get_user_badges(db_user.badges)
    )
    return response_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert badges JSON to list for response
    response_user = UserResponse(
        id=user.id,
        name=user.name,
        points=user.points,
        rank=user.rank,
        donations_count=user.donations_count,
        badges=get_user_badges(user.badges)
    )
    return response_user

@app.get("/users/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    
    # Convert badges for each user
    response_users = []
    for user in users:
        response_users.append(UserResponse(
            id=user.id,
            name=user.name,
            points=user.points,
            rank=user.rank,
            donations_count=user.donations_count,
            badges=get_user_badges(user.badges)
        ))
    
    return response_users

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

# Leaderboard endpoint
@app.get("/leaderboard/", response_model=List[LeaderboardEntry])
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get top users ranked by points"""
    users = db.query(User).order_by(User.points.desc()).limit(limit).all()
    
    leaderboard = []
    for user in users:
        leaderboard.append(LeaderboardEntry(
            user_id=user.id,
            name=user.name,
            points=user.points,
            rank=user.rank,
            donations_count=user.donations_count,
            badges=get_user_badges(user.badges)
        ))
    
    return leaderboard

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

def get_user_badges(badges_json: str) -> List[str]:
    """Parse badges JSON string to list"""
    if not badges_json or badges_json is None:
        return []
    try:
        return json.loads(badges_json)
    except:
        return []

def set_user_badges(badges: List[str]) -> str:
    """Convert badges list to JSON string"""
    return json.dumps(badges)

def check_and_award_badges(user: User, db: Session) -> List[str]:
    """Check achievements and award new badges"""
    current_badges = get_user_badges(user.badges)
    new_badges = []
    
    # Achievement 1: First Donation
    if user.donations_count >= 1 and "First Blood" not in current_badges:
        current_badges.append("First Blood")
        new_badges.append("First Blood")
    
    # Achievement 2: Generous Giver (10 donations)
    if user.donations_count >= 10 and "Generous Giver" not in current_badges:
        current_badges.append("Generous Giver")
        new_badges.append("Generous Giver")
    
    # Achievement 3: Point Milestone (1000 points)
    if user.points >= 1000 and "Point Master" not in current_badges:
        current_badges.append("Point Master")
        new_badges.append("Point Master")
    
    # Achievement 4: High Roller (Single donation worth 200+ points)
    if "High Roller" not in current_badges:
        high_value_donation = db.query(Donation).filter(
            Donation.user_id == user.id,
            Donation.points_awarded >= 200
        ).first()
        if high_value_donation:
            current_badges.append("High Roller")
            new_badges.append("High Roller")
    
    # Achievement 5: Rank Up badges
    rank_badges = {
        "Silver": "Silver Star",
        "Gold": "Golden Hero", 
        "Platinum": "Platinum Champion",
        "Diamond": "Diamond Legend"
    }
    
    if user.rank in rank_badges:
        badge_name = rank_badges[user.rank]
        if badge_name not in current_badges:
            current_badges.append(badge_name)
            new_badges.append(badge_name)
    
    # Achievement 6: Lifesaver (Medical supplies donation)
    if "Lifesaver" not in current_badges:
        medical_donation = db.query(Donation).filter(
            Donation.user_id == user.id,
            Donation.item_type == "medical_supplies"
        ).first()
        if medical_donation:
            current_badges.append("Lifesaver")
            new_badges.append("Lifesaver")
    
    # Update user badges
    user.badges = set_user_badges(current_badges)
    
    return new_badges

@app.post("/donate", response_model=DonateResponse)
def donate(request: DonateRequest, db: Session = Depends(get_db)):
    # Validate user exists
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Store old rank for comparison
    old_rank = user.rank
    
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
    
    # IMPORTANT: Commit the donation first so badge checks can see it
    db.commit()
    db.refresh(user)
    
    # Now check for new badges and achievements (after donation is committed)
    new_badges = check_and_award_badges(user, db)
    
    # Commit badge updates
    db.commit()
    db.refresh(user)
    
    # Log rank changes and new badges (optional - for debugging)
    if user.rank != old_rank:
        print(f"🎉 User {user.name} ranked up from {old_rank} to {user.rank}!")
    
    if new_badges:
        print(f"🏅 User {user.name} earned new badges: {', '.join(new_badges)}")
    
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

if __name__ == "__main__":
    import uvicorn
    import socket
    
    def find_free_port():
        """Find a free port starting from 8000"""
        for port in range(8000, 8010):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return 8000  # fallback
    
    port = find_free_port()
    print(f"🚀 Starting Donation Platform API on port {port}")
    print(f"📖 Interactive docs: http://localhost:{port}/docs")
    print(f"❤️  Health check: http://localhost:{port}/ping")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
