from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExerciseBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    muscle_groups: Optional[str] = None
    difficulty: Optional[str] = None
    exercise_type: Optional[str] = None
    equipment_required: Optional[str] = None
    instructions: Optional[str] = None
    progression_level: int
    estimated_duration: int

    class Config:
        from_attributes = True

class WorkoutExerciseResponse(BaseModel):
    id: int
    exercise: ExerciseBase
    sets: int
    reps: int
    duration: Optional[int] = None
    rest_time: int
    order: int

    class Config:
        from_attributes = True

class WorkoutPlanResponse(BaseModel):
    id: int
    date: datetime
    duration: Optional[int] = None
    difficulty: Optional[str] = None
    goal: Optional[str] = None
    recovery_level: Optional[int] = None
    reasoning: Optional[str] = None
    exercises: List[WorkoutExerciseResponse] = []

    class Config:
        from_attributes = True

class WorkoutCompleteRequest(BaseModel):
    completion_percentage: int
    actual_duration: int
    user_rating: int
    energy_before: int
    energy_after: int
    notes: Optional[str] = None

class FitnessGenerateRequest(BaseModel):
    available_time: Optional[int] = None
    energy: Optional[int] = None
    goal: Optional[str] = None
