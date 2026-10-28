from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DailyCheckInRequest(BaseModel):
    energy: int
    stress: int
    mood: int
    productivity: int
    notes: Optional[str] = None

class DailyCheckInResponse(BaseModel):
    id: int
    date: datetime
    energy: int
    stress: int
    mood: int
    productivity: int
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class SleepRecordRequest(BaseModel):
    bedtime: str
    wake_time: str
    sleep_duration: float
    sleep_quality: str

class SleepRecordResponse(BaseModel):
    id: int
    date: datetime
    bedtime: str
    wake_time: str
    sleep_duration: float
    sleep_quality: str

    class Config:
        from_attributes = True

class HabitBase(BaseModel):
    name: str
    category: str
    target_frequency: str = "Daily"

class HabitResponse(BaseModel):
    id: int
    name: str
    category: str
    is_active: bool
    target_frequency: str

    class Config:
        from_attributes = True

class LifestyleSummaryResponse(BaseModel):
    lifestyle_score: int
    recovery_score: int
    sleep_duration: float
    active_habits_count: int
    completed_habits_today: int
    energy: int
    stress: int
    ai_insight: str
