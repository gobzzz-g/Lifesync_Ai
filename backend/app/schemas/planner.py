from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LifeStateResponse(BaseModel):
    fitness: int
    nutrition: int
    lifestyle: int
    recovery: int
    career: int
    energy: int
    stress: int
    sleep_hours: float
    available_time: int

class LifeBalanceResponse(BaseModel):
    overall_growth: int
    balance_score: int
    reason: str
    lowest_domain: str
    highest_domain: str

class CrossDomainInsightResponse(BaseModel):
    insight: str
    recommendation: str

class DailyPlanTaskResponse(BaseModel):
    id: int
    title: str
    category: str
    duration: int
    priority: str
    source_module: Optional[str]
    is_completed: bool
    flexible: bool

    class Config:
        from_attributes = True

class DailyPlanResponse(BaseModel):
    id: int
    date: datetime
    energy_level: Optional[int]
    available_time: int
    overall_priority: str
    status: str
    tasks: List[DailyPlanTaskResponse]

    class Config:
        from_attributes = True

class PlannerFeedbackRequest(BaseModel):
    feeling: str
    notes: Optional[str] = None
