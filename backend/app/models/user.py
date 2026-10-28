import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    onboarding_completed = Column(Boolean, default=False)
    
    # Basic / Fitness
    gender = Column(String, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    fitness_level = Column(String, nullable=True)
    fitness_goal = Column(String, nullable=True)
    workout_frequency = Column(String, nullable=True)
    preferred_training_type = Column(String, nullable=True)
    calisthenics_skill_goals = Column(String, nullable=True)
    current_abilities = Column(String, nullable=True)
    available_workout_time = Column(String, nullable=True)
    equipment_availability = Column(String, nullable=True)
    
    # Nutrition
    nutrition_goal = Column(String, nullable=True)
    food_preferences = Column(String, nullable=True)
    dietary_preferences = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    foods_to_avoid = Column(String, nullable=True)
    food_budget = Column(String, nullable=True)
    meals_per_day = Column(Integer, nullable=True)
    
    # Lifestyle
    available_free_time = Column(String, nullable=True)
    habit_preferences = Column(String, nullable=True)
    wake_up_time = Column(String, nullable=True)
    sleep_time = Column(String, nullable=True)
    sleep_duration = Column(Float, nullable=True)
    daily_work_hours = Column(Float, nullable=True)
    daily_screen_time = Column(Float, nullable=True)
    water_intake = Column(String, nullable=True)
    daily_activity_level = Column(String, nullable=True)
    break_frequency = Column(String, nullable=True)
    
    # Well-being
    stress_level = Column(Integer, nullable=True)
    energy_level = Column(Integer, nullable=True)
    productivity_level = Column(Integer, nullable=True)
    daily_mood = Column(Integer, nullable=True)

    # Career
    career_status = Column(String, nullable=True)
    career_goal = Column(String, nullable=True)
    target_career = Column(String, nullable=True)
    current_skills = Column(String, nullable=True)
    career_experience_level = Column(String, nullable=True)
    available_learning_time = Column(String, nullable=True)
    preferred_learning_style = Column(String, nullable=True)
    
    # AI Preferences
    recommendation_frequency = Column(String, nullable=True)
    daily_plan_generation = Column(Boolean, default=True)
    fitness_reminders = Column(Boolean, default=True)
    nutrition_reminders = Column(Boolean, default=True)
    habit_reminders = Column(Boolean, default=True)
    career_reminders = Column(Boolean, default=True)
    
    # Generated Scores & Insights
    fitness_score = Column(Integer, nullable=True)
    nutrition_score = Column(Integer, nullable=True)
    lifestyle_score = Column(Integer, nullable=True)
    well_being_score = Column(Integer, nullable=True)
    career_score = Column(Integer, nullable=True)
    overall_score = Column(Integer, nullable=True)
    
    ai_insights = Column(String, nullable=True)  # JSON string
    ai_priorities = Column(String, nullable=True) # JSON string
    
    # Gamification
    xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    achievements = Column(String, default="[]") # JSON string array
    last_active_date = Column(DateTime, nullable=True)

    # Nutrition Tracking
    target_calories = Column(Integer, nullable=True)
    target_protein = Column(Integer, nullable=True)
    target_carbs = Column(Integer, nullable=True)
    target_fats = Column(Integer, nullable=True)
    water_target = Column(Integer, default=2500) # ml
    water_consumed = Column(Integer, default=0)  # ml, resets daily ideally

    user = relationship("User", back_populates="profile")
