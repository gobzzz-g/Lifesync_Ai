from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SkillBase(BaseModel):
    name: str
    proficiency_level: str

class UserSkillResponse(BaseModel):
    id: int
    name: str
    proficiency_level: str
    
    class Config:
        from_attributes = True

class CareerGoalRequest(BaseModel):
    target_role: str
    available_learning_time: int # minutes

class CareerGoalResponse(BaseModel):
    id: int
    target_role: str
    available_learning_time: int
    
    class Config:
        from_attributes = True

class RoadmapTaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    skill: Optional[str] = None
    estimated_minutes: int
    is_completed: bool

    class Config:
        from_attributes = True

class RoadmapResponse(BaseModel):
    id: int
    target_role: str
    tasks: List[RoadmapTaskResponse]

    class Config:
        from_attributes = True

class CareerGapAnalysisResponse(BaseModel):
    readiness_score: int
    strong_skills: List[str]
    improving_skills: List[str]
    missing_skills: List[str]
    priority_skills: List[str]

class ResumeAnalysisResponse(BaseModel):
    score: int
    strengths: List[str]
    missing_skills: List[str]
    improvement_suggestions: List[str]

class JobAnalysisRequest(BaseModel):
    job_description: str

class JobAnalysisResponse(BaseModel):
    match_percentage: int
    matching_skills: List[str]
    missing_skills: List[str]
    recommended_improvements: List[str]

class MockInterviewRequest(BaseModel):
    role: str
    interview_type: str

class MockInterviewResponse(BaseModel):
    id: int
    question: str

class MockInterviewAnswer(BaseModel):
    answer: str

class MockInterviewFeedback(BaseModel):
    score: int
    feedback: str
    strong_areas: List[str]
    weak_areas: List[str]
    recommended_topics: List[str]

class InterviewHistoryResponse(BaseModel):
    id: int
    role: str
    interview_type: str
    score: int
    date: datetime

    class Config:
        from_attributes = True
