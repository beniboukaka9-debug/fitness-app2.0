"""Workout and Exercise data models"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import List

Base = declarative_base()

class Exercise(Base):
    """Exercise database model"""
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    target_area = Column(String)  # "arms", "abs", "legs", "back", "chest", "full_body"
    difficulty = Column(String)  # "beginner", "intermediate", "advanced"
    duration = Column(Integer)  # seconds per set
    sets = Column(Integer, default=3)
    rest_time = Column(Integer, default=60)  # seconds between sets
    equipment_needed = Column(String, nullable=True)  # "bodyweight", "dumbbells", "bands", etc.
    image_url = Column(String, nullable=True)  # GIF or image
    instructions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Workout(Base):
    """Workout session database model"""
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    target_area = Column(String)  # "arms", "abs", "full_body", etc.
    difficulty = Column(String)  # "beginner", "intermediate", "advanced"
    duration = Column(Integer)  # total duration in seconds
    exercises_json = Column(Text)  # JSON array of exercise IDs and modifications
    total_calories_burned = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic schemas
class ExerciseResponse(BaseModel):
    """Exercise response schema"""
    id: int
    name: str
    description: str
    target_area: str
    difficulty: str
    duration: int
    sets: int
    rest_time: int
    equipment_needed: str | None
    image_url: str | None
    instructions: str | None
    
    class Config:
        from_attributes = True

class WorkoutCreate(BaseModel):
    """Workout creation schema"""
    target_area: str  # "arms", "abs", "full_body"
    difficulty: str | None = "beginner"
    duration: int | None = 1800  # 30 minutes default
    available_equipment: List[str] = ["bodyweight"]  # "bodyweight", "dumbbells", "bands"

class WorkoutResponse(BaseModel):
    """Workout response schema"""
    id: int
    user_id: int
    name: str
    target_area: str
    difficulty: str
    duration: int
    exercises_json: str
    is_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
