"""CRUD operations for database models"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from app.models.user import User, UserCreate, UserUpdate
from app.models.activity import Activity, ActivityCreate
from app.models.workout import Exercise, Workout
from passlib.context import CryptContext
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============ USER OPERATIONS ============

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=pwd_context.hash(user.password),
        age=user.age,
        weight=user.weight,
        height=user.height,
        gender=user.gender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User | None:
    """Update user profile"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db_user.updated_at = datetime.utcnow()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ============ ACTIVITY OPERATIONS ============

def create_activity(db: Session, user_id: int, activity: ActivityCreate) -> Activity:
    """Create a new activity"""
    db_activity = Activity(
        user_id=user_id,
        activity_type=activity.activity_type,
        step_count=activity.step_count,
        distance=activity.distance,
        duration=activity.duration,
        calories_burned=activity.calories_burned,
        average_pace=activity.average_pace,
        start_time=activity.start_time,
        end_time=activity.end_time,
        gps_data=activity.gps_data
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_today_activities(db: Session, user_id: int) -> list[Activity]:
    """Get today's activities for a user"""
    today = datetime.utcnow().date()
    return db.query(Activity).filter(
        Activity.user_id == user_id,
        Activity.created_at >= datetime.combine(today, datetime.min.time())
    ).all()

def get_week_activities(db: Session, user_id: int) -> list[Activity]:
    """Get last 7 days activities for a user"""
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    return db.query(Activity).filter(
        Activity.user_id == user_id,
        Activity.created_at >= seven_days_ago
    ).order_by(desc(Activity.created_at)).all()

def get_total_steps_today(db: Session, user_id: int) -> int:
    """Get total steps for today"""
    today = datetime.utcnow().date()
    activities = db.query(Activity).filter(
        Activity.user_id == user_id,
        Activity.created_at >= datetime.combine(today, datetime.min.time()),
        Activity.activity_type.in_(["steps", "walk", "run"])
    ).all()
    return sum(a.step_count for a in activities)

# ============ EXERCISE OPERATIONS ============

def get_exercises_by_target_area(db: Session, target_area: str) -> list[Exercise]:
    """Get exercises by target area"""
    return db.query(Exercise).filter(
        (Exercise.target_area == target_area) | 
        (Exercise.target_area == "full_body")
    ).all()

def get_exercises_by_equipment(db: Session, equipment: list[str]) -> list[Exercise]:
    """Get exercises that match available equipment"""
    exercises = []
    for eq in equipment:
        exercises.extend(
            db.query(Exercise).filter(
                (Exercise.equipment_needed == eq) | 
                (Exercise.equipment_needed == "bodyweight")
            ).all()
        )
    return list(set(exercises))  # Remove duplicates

def create_workout(db: Session, user_id: int, name: str, target_area: str, 
                  difficulty: str, duration: int, exercises_json: str) -> Workout:
    """Create a new workout"""
    db_workout = Workout(
        user_id=user_id,
        name=name,
        target_area=target_area,
        difficulty=difficulty,
        duration=duration,
        exercises_json=exercises_json
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

def get_user_workouts(db: Session, user_id: int, limit: int = 10) -> list[Workout]:
    """Get user's recent workouts"""
    return db.query(Workout).filter(
        Workout.user_id == user_id
    ).order_by(desc(Workout.created_at)).limit(limit).all()

def complete_workout(db: Session, workout_id: int, calories_burned: float = 0.0) -> Workout | None:
    """Mark workout as completed"""
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not db_workout:
        return None
    
    db_workout.is_completed = True
    db_workout.end_time = datetime.utcnow()
    if calories_burned > 0:
        db_workout.total_calories_burned = calories_burned
    
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout
