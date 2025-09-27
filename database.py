from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./donation_platform.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    points = Column(Integer, default=0)
    rank = Column(String, default="Bronze")
    donations_count = Column(Integer, default=0)
    badges = Column(String, default="")  # JSON string of earned badges
    
    donations = relationship("Donation", back_populates="user")

class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String, index=True)
    location = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    points_awarded = Column(Integer)
    
    user = relationship("User", back_populates="donations")

class Need(Base):
    __tablename__ = "needs"
    
    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String, index=True, unique=True)
    urgency_level = Column(String)  # "low", "medium", "high", "critical"
    multiplier = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
