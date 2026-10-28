from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
import datetime
from app.db.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, nullable=True) # Frontend, Backend, Soft Skills
    description = Column(Text, nullable=True)

class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    proficiency_level = Column(String, default="Beginner") # Beginner, Intermediate, Advanced
    
class CareerGoal(Base):
    __tablename__ = "career_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    target_role = Column(String, nullable=False)
    target_industry = Column(String, nullable=True)
    available_learning_time = Column(Integer, default=60) # minutes per day
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    target_role = Column(String, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    tasks = relationship("RoadmapTask", back_populates="roadmap", cascade="all, delete-orphan")

class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    skill = Column(String, nullable=True)
    estimated_minutes = Column(Integer, default=30)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    roadmap = relationship("Roadmap", back_populates="tasks")

class InterviewHistory(Base):
    __tablename__ = "interview_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)
    interview_type = Column(String, nullable=False) # Technical, HR
    score = Column(Integer, default=0)
    feedback = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
