import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    muscle_groups = Column(String, nullable=True)  # Comma-separated
    difficulty = Column(String, nullable=True)     # Beginner, Intermediate, Advanced
    exercise_type = Column(String, nullable=True)  # Strength, Cardio, Mobility
    equipment_required = Column(String, nullable=True) # None, Pull-up bar, Resistance bands
    instructions = Column(Text, nullable=True)
    progression_level = Column(Integer, default=1)
    estimated_duration = Column(Integer, default=60) # seconds per set
    
    # Form Guidance
    form_setup = Column(Text, nullable=True)
    form_movement = Column(Text, nullable=True)
    form_breathing = Column(Text, nullable=True)
    common_mistakes = Column(Text, nullable=True)
    regression = Column(String, nullable=True)
    progression = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    duration = Column(Integer, nullable=True) # estimated minutes
    difficulty = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    recovery_level = Column(Integer, nullable=True) # 0-100
    reasoning = Column(Text, nullable=True) # AI reasoning for this workout
    generated_by = Column(String, default="AdaptiveFitnessEngine")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    exercises = relationship("WorkoutExercise", back_populates="plan", cascade="all, delete-orphan")

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer, default=3)
    reps = Column(Integer, default=10)
    duration = Column(Integer, nullable=True) # seconds if timed (like plank)
    rest_time = Column(Integer, default=60) # seconds
    difficulty = Column(String, nullable=True)
    order = Column(Integer, default=0)
    
    plan = relationship("WorkoutPlan", back_populates="exercises")
    exercise = relationship("Exercise")

class WorkoutHistory(Base):
    __tablename__ = "workout_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=True)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)
    completion_percentage = Column(Integer, default=100)
    actual_duration = Column(Integer, nullable=True) # minutes
    user_rating = Column(Integer, nullable=True) # 1-10 difficulty rating
    energy_before = Column(Integer, nullable=True) # 1-10
    energy_after = Column(Integer, nullable=True) # 1-10
    notes = Column(Text, nullable=True)

class FitnessMetrics(Base):
    __tablename__ = "fitness_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    steps = Column(Integer, nullable=True)
    heart_rate = Column(Integer, nullable=True) # resting HR
    sleep_duration = Column(Float, nullable=True) # hours
    activity_minutes = Column(Integer, nullable=True)
    recovery_score = Column(Integer, nullable=True)
    energy_level = Column(Integer, nullable=True)
