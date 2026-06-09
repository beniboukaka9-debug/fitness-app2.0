"""Workout API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.workout import WorkoutCreate, WorkoutResponse
from app.database.crud import get_user_workouts, complete_workout, create_workout
from app.services.workout_generator import WorkoutGenerator
import json

router = APIRouter(prefix="/api/v1/workouts", tags=["workouts"])

@router.post("/generate")
def generate_workout(user_id: int, workout_request: WorkoutCreate, db: Session = Depends(get_db)):
    """Generate an AI-powered personalized workout"""
    generator = WorkoutGenerator(db=db)
    
    recommendation = generator.generate_recommendation(
        user_id=user_id,
        user_data={
            'target_area': workout_request.target_area,
            'difficulty': workout_request.difficulty or 'beginner',
            'duration': workout_request.duration or 1800,
            'available_equipment': workout_request.available_equipment
        }
    )
    
    # Create workout in database
    workout = create_workout(
        db=db,
        user_id=user_id,
        name=recommendation['name'],
        target_area=recommendation['target_area'],
        difficulty=recommendation['difficulty'],
        duration=recommendation['duration'],
        exercises_json=recommendation['exercises_json']
    )
    
    return {
        "workout": {
            "id": workout.id,
            "name": workout.name,
            "target_area": workout.target_area,
            "difficulty": workout.difficulty,
            "duration": workout.duration,
            "created_at": workout.created_at
        },
        "exercises": recommendation['exercises'],
        "intensity_modifier": recommendation['intensity_modifier']
    }

@router.get("/my-workouts")
def get_my_workouts(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get user's recent workouts"""
    workouts = get_user_workouts(db=db, user_id=user_id, limit=limit)
    return [
        {
            "id": w.id,
            "name": w.name,
            "target_area": w.target_area,
            "difficulty": w.difficulty,
            "duration": w.duration,
            "is_completed": w.is_completed,
            "created_at": w.created_at
        }
        for w in workouts
    ]

@router.put("/{workout_id}/complete")
def complete_workout_endpoint(workout_id: int, calories_burned: float = 0.0, db: Session = Depends(get_db)):
    """Mark a workout as completed"""
    workout = complete_workout(db=db, workout_id=workout_id, calories_burned=calories_burned)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    return {
        "id": workout.id,
        "name": workout.name,
        "is_completed": workout.is_completed,
        "end_time": workout.end_time,
        "total_calories_burned": workout.total_calories_burned
    }
