"""AI-powered workout generator using machine learning"""
import json
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sklearn.neighbors import NearestNeighbors
import numpy as np
from app.models.workout import Exercise, Workout
from app.models.activity import Activity
from app.database.crud import (
    get_exercises_by_target_area,
    get_exercises_by_equipment,
    create_workout,
    get_week_activities
)

class WorkoutGenerator:
    """Generate personalized workouts based on user profile and recent activity"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_recommendation(self, user_id: int, user_data: dict) -> dict:
        """
        Generate personalized workout recommendation
        
        Args:
            user_id: User ID
            user_data: {
                'target_area': 'arms|abs|full_body|legs|back|chest',
                'difficulty': 'beginner|intermediate|advanced',
                'duration': int (seconds),
                'available_equipment': ['bodyweight', 'dumbbells', 'bands']
            }
        """
        # Get user's recent activity to determine intensity
        recent_activities = get_week_activities(self.db, user_id)
        intensity_modifier = self._calculate_intensity_modifier(recent_activities)
        
        # Adjust difficulty based on recent activity
        recommended_difficulty = self._adjust_difficulty(user_data.get('difficulty'), intensity_modifier)
        
        # Get matching exercises
        target_area = user_data.get('target_area', 'full_body')
        available_equipment = user_data.get('available_equipment', ['bodyweight'])
        duration = user_data.get('duration', 1800)  # 30 minutes default
        
        # Fetch exercises
        exercises = self._select_exercises(
            target_area=target_area,
            difficulty=recommended_difficulty,
            equipment=available_equipment,
            total_duration=duration
        )
        
        # Create workout
        workout_name = self._generate_workout_name(target_area, recommended_difficulty)
        exercises_json = json.dumps([
            {
                'id': ex.id,
                'name': ex.name,
                'sets': ex.sets,
                'duration': ex.duration,
                'rest_time': ex.rest_time
            } for ex in exercises
        ])
        
        return {
            'name': workout_name,
            'target_area': target_area,
            'difficulty': recommended_difficulty,
            'duration': duration,
            'exercises': [
                {
                    'id': ex.id,
                    'name': ex.name,
                    'description': ex.description,
                    'sets': ex.sets,
                    'duration': ex.duration,
                    'rest_time': ex.rest_time,
                    'instructions': ex.instructions,
                    'image_url': ex.image_url
                } for ex in exercises
            ],
            'intensity_modifier': intensity_modifier,
            'exercises_json': exercises_json
        }
    
    def _calculate_intensity_modifier(self, recent_activities: list[Activity]) -> float:
        """
        Calculate intensity modifier based on recent activity
        Returns value between 0.5 (light) and 1.5 (intense)
        """
        if not recent_activities:
            return 1.0  # Default to normal
        
        # Calculate total activity in last 7 days
        total_duration = sum(a.duration for a in recent_activities)
        total_distance = sum(a.distance for a in recent_activities)
        
        # If user had significant activity, reduce workout intensity
        if total_distance > 50 or total_duration > 7200:  # 50km or 2 hours
            return 0.7  # Light workout suggested
        elif total_distance < 10 and total_duration < 1800:  # Less than 10km or 30 min
            return 1.3  # More intense workout suggested
        else:
            return 1.0  # Normal intensity
    
    def _adjust_difficulty(self, base_difficulty: str, intensity_modifier: float) -> str:
        """
        Adjust difficulty level based on intensity modifier
        """
        difficulty_mapping = {
            'beginner': 0,
            'intermediate': 1,
            'advanced': 2
        }
        reverse_mapping = {0: 'beginner', 1: 'intermediate', 2: 'advanced'}
        
        base_level = difficulty_mapping.get(base_difficulty, 1)
        
        # Adjust based on intensity modifier
        if intensity_modifier < 0.8:
            adjusted_level = max(0, base_level - 1)
        elif intensity_modifier > 1.2:
            adjusted_level = min(2, base_level + 1)
        else:
            adjusted_level = base_level
        
        return reverse_mapping[adjusted_level]
    
    def _select_exercises(self, target_area: str, difficulty: str, 
                         equipment: list[str], total_duration: int) -> list[Exercise]:
        """
        Select exercises that fit the target area, difficulty, and total duration
        """
        # Get exercises by target area and difficulty
        all_exercises = self.db.query(Exercise).filter(
            ((Exercise.target_area == target_area) | (Exercise.target_area == 'full_body')),
            Exercise.difficulty == difficulty
        ).all()
        
        # Filter by available equipment
        filtered_exercises = [
            ex for ex in all_exercises
            if ex.equipment_needed in equipment or ex.equipment_needed == 'bodyweight'
        ]
        
        # Select exercises to fit duration
        selected = []
        current_duration = 0
        
        for ex in filtered_exercises:
            exercise_duration = (ex.duration * ex.sets) + (ex.rest_time * (ex.sets - 1))
            if current_duration + exercise_duration <= total_duration:
                selected.append(ex)
                current_duration += exercise_duration
        
        # If not enough exercises, add some random ones
        if len(selected) < 3 and len(filtered_exercises) > len(selected):
            remaining = [ex for ex in filtered_exercises if ex not in selected]
            selected.extend(random.sample(remaining, min(3 - len(selected), len(remaining))))
        
        return selected[:6]  # Max 6 exercises per workout
    
    def _generate_workout_name(self, target_area: str, difficulty: str) -> str:
        """
        Generate a descriptive workout name
        """
        difficulty_prefix = {
            'beginner': '🔰 Beginner',
            'intermediate': '💪 Intermediate',
            'advanced': '🔥 Advanced'
        }
        
        target_suffixes = {
            'arms': 'Arm Blast',
            'abs': 'Core Crusher',
            'legs': 'Leg Day',
            'back': 'Back Strength',
            'chest': 'Chest Day',
            'full_body': 'Full Body Burn'
        }
        
        prefix = difficulty_prefix.get(difficulty, '💪')
        suffix = target_suffixes.get(target_area, 'Workout')
        
        return f"{prefix} {suffix}"
