"""User data model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel, EmailStr

Base = declarative_base()

class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)  # kg
    height = Column(Float, nullable=True)  # cm
    gender = Column(String, nullable=True)  # M/F
    fitness_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    daily_step_goal = Column(Integer, default=10000)
    stride_length = Column(Float, default=0.78)  # meters (average)
    preferred_workout_areas = Column(String, default="full_body")  # comma-separated
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic schemas for API
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str
    age: int | None = None
    weight: float | None = None
    height: float | None = None
    gender: str | None = None

class UserCreate(UserBase):
    """User creation schema"""
    password: str

class UserUpdate(BaseModel):
    """User update schema"""
    full_name: str | None = None
    weight: float | None = None
    height: float | None = None
    fitness_level: str | None = None
    daily_step_goal: int | None = None
    stride_length: float | None = None
    preferred_workout_areas: str | None = None

class UserResponse(UserBase):
    """User response schema"""
    id: int
    fitness_level: str
    daily_step_goal: int
    stride_length: float
    created_at: datetime
    
    class Config:
        from_attributes = True
