"""Activity (step tracking, running) data model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

class Activity(Base):
    """Activity database model (steps, runs, etc.)"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    activity_type = Column(String)  # "run", "walk", "steps"
    step_count = Column(Integer, default=0)
    distance = Column(Float, default=0.0)  # km
    duration = Column(Integer, default=0)  # seconds
    calories_burned = Column(Float, default=0.0)
    average_pace = Column(Float, nullable=True)  # min/km for runs
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    gps_data = Column(String, nullable=True)  # JSON string of lat/lon points
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Computed field for display
    @property
    def duration_minutes(self):
        """Get duration in minutes"""
        return self.duration // 60 if self.duration else 0

class ActivityCreate(BaseModel):
    """Activity creation schema"""
    activity_type: str
    step_count: int = 0
    distance: float = 0.0
    duration: int = 0
    calories_burned: float = 0.0
    average_pace: float | None = None
    start_time: datetime
    end_time: datetime | None = None
    gps_data: str | None = None

class ActivityResponse(BaseModel):
    """Activity response schema"""
    id: int
    user_id: int
    activity_type: str
    step_count: int
    distance: float
    duration: int
    calories_burned: float
    average_pace: float | None
    start_time: datetime
    end_time: datetime | None
    is_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
