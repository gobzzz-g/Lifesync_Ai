from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from app.db.database import Base

class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    energy_level = Column(Integer, nullable=True) # captured at generation time
    available_time = Column(Integer, default=120) # total free minutes
    overall_priority = Column(String, default="Balanced") # e.g. "Recovery", "Career", "Fitness"
    status = Column(String, default="Active")

    tasks = relationship("DailyPlanTask", back_populates="plan", cascade="all, delete-orphan")

class DailyPlanTask(Base):
    __tablename__ = "daily_plan_tasks"

    id = Column(Integer, primary_key=True, index=True)
    daily_plan_id = Column(Integer, ForeignKey("daily_plans.id"), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False) # e.g. "Fitness", "Career", "Nutrition", "Lifestyle"
    start_time = Column(String, nullable=True) # e.g. "07:00"
    end_time = Column(String, nullable=True) # e.g. "07:30"
    duration = Column(Integer, default=30) # minutes
    priority = Column(String, default="Medium")
    source_module = Column(String, nullable=True) # Module generating it
    is_completed = Column(Boolean, default=False)
    flexible = Column(Boolean, default=True) # If it can be moved around
    
    plan = relationship("DailyPlan", back_populates="tasks")

class PlanFeedback(Base):
    __tablename__ = "plan_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    daily_plan_id = Column(Integer, ForeignKey("daily_plans.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    feeling = Column(String, nullable=False) # Too easy, Balanced, Too busy, Too difficult
    notes = Column(Text, nullable=True)
