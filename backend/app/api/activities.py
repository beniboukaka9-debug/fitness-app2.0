"""Activity API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.db import get_db
from app.models.activity import ActivityCreate, ActivityResponse
from app.database.crud import (
    create_activity,
    get_today_activities,
    get_week_activities,
    get_total_steps_today
)

router = APIRouter(prefix="/api/v1/activities", tags=["activities"])

@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def log_activity(user_id: int, activity: ActivityCreate, db: Session = Depends(get_db)):
    """Log a new activity (steps, run, walk, etc.)"""
    return create_activity(db=db, user_id=user_id, activity=activity)

@router.get("/today", response_model=list[ActivityResponse])
def get_today(user_id: int, db: Session = Depends(get_db)):
    """Get today's activities for a user"""
    return get_today_activities(db=db, user_id=user_id)

@router.get("/week", response_model=list[ActivityResponse])
def get_week(user_id: int, db: Session = Depends(get_db)):
    """Get last 7 days of activities"""
    return get_week_activities(db=db, user_id=user_id)

@router.get("/steps-today")
def steps_today(user_id: int, db: Session = Depends(get_db)):
    """Get total steps for today"""
    total_steps = get_total_steps_today(db=db, user_id=user_id)
    return {"total_steps": total_steps, "date": datetime.utcnow().date()}

@router.get("/summary")
def activity_summary(user_id: int, db: Session = Depends(get_db)):
    """Get activity summary for the week"""
    activities = get_week_activities(db=db, user_id=user_id)
    
    total_steps = sum(a.step_count for a in activities)
    total_distance = sum(a.distance for a in activities)
    total_calories = sum(a.calories_burned for a in activities)
    total_duration = sum(a.duration for a in activities) // 60  # in minutes
    
    return {
        "total_steps": total_steps,
        "total_distance": total_distance,
        "total_calories": total_calories,
        "total_duration_minutes": total_duration,
        "activity_count": len(activities),
        "week_average_daily_steps": total_steps // 7 if activities else 0
    }
