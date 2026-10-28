from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ProfileBase(BaseModel):
    onboarding_completed: Optional[bool] = False
    
    # Basic / Fitness
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_level: Optional[str] = None
    fitness_goal: Optional[str] = None
    workout_frequency: Optional[str] = None
    preferred_training_type: Optional[str] = None
    calisthenics_skill_goals: Optional[str] = None
    current_abilities: Optional[str] = None
    available_workout_time: Optional[str] = None
    equipment_availability: Optional[str] = None
    
    # Nutrition
    nutrition_goal: Optional[str] = None
    food_preferences: Optional[str] = None
    dietary_preferences: Optional[str] = None
    allergies: Optional[str] = None
    foods_to_avoid: Optional[str] = None
    food_budget: Optional[str] = None
    meals_per_day: Optional[int] = None
    
    # Lifestyle
    available_free_time: Optional[str] = None
    habit_preferences: Optional[str] = None
    wake_up_time: Optional[str] = None
    sleep_time: Optional[str] = None
    sleep_duration: Optional[float] = None
    daily_work_hours: Optional[float] = None
    daily_screen_time: Optional[float] = None
    water_intake: Optional[str] = None
    daily_activity_level: Optional[str] = None
    break_frequency: Optional[str] = None
    
    # Well-being
    stress_level: Optional[int] = None
    energy_level: Optional[int] = None
    productivity_level: Optional[int] = None
    daily_mood: Optional[int] = None

    # Career
    career_status: Optional[str] = None
    career_goal: Optional[str] = None
    target_career: Optional[str] = None
    current_skills: Optional[str] = None
    career_experience_level: Optional[str] = None
    available_learning_time: Optional[str] = None
    preferred_learning_style: Optional[str] = None
    
    # AI Preferences
    recommendation_frequency: Optional[str] = None
    daily_plan_generation: Optional[bool] = None
    fitness_reminders: Optional[bool] = None
    nutrition_reminders: Optional[bool] = None
    habit_reminders: Optional[bool] = None
    career_reminders: Optional[bool] = None
    
    # Generated Scores & Insights
    fitness_score: Optional[int] = None
    nutrition_score: Optional[int] = None
    lifestyle_score: Optional[int] = None
    well_being_score: Optional[int] = None
    career_score: Optional[int] = None
    overall_score: Optional[int] = None
    
    ai_insights: Optional[str] = None
    ai_priorities: Optional[str] = None

    target_calories: Optional[int] = None
    target_protein: Optional[int] = None
    target_carbs: Optional[int] = None
    target_fats: Optional[int] = None
    water_target: Optional[int] = None
    water_consumed: Optional[int] = None


class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
