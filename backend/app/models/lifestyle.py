import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class SleepRecord(Base):
    __tablename__ = "sleep_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    bedtime = Column(String, nullable=True) # e.g. "22:30"
    wake_time = Column(String, nullable=True) # e.g. "06:30"
    sleep_duration = Column(Float, default=0.0) # hours
    sleep_quality = Column(String, nullable=True) # Good, Fair, Poor
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DailyActivity(Base):
    __tablename__ = "daily_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    steps = Column(Integer, default=0)
    active_minutes = Column(Integer, default=0)
    sedentary_minutes = Column(Integer, default=0)
    screen_time = Column(Float, default=0.0) # hours
    study_hours = Column(Float, default=0.0)
    work_hours = Column(Float, default=0.0)
    breaks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True) # Health, Productivity, Mindfulness
    target_frequency = Column(String, default="Daily")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    habit = relationship("Habit", back_populates="logs")

class DailyCheckIn(Base):
    __tablename__ = "daily_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    energy = Column(Integer, default=5) # 1-10
    stress = Column(Integer, default=5) # 1-10
    mood = Column(Integer, default=5) # 1-10
    productivity = Column(Integer, default=5) # 1-10
    notes = Column(Text, nullable=True)
