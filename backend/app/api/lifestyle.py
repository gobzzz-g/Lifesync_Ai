from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date, timedelta
from app.db.database import get_db
from app.models.user import User, UserProfile
from app.models.lifestyle import SleepRecord, DailyCheckIn, Habit, HabitLog
from app.schemas.lifestyle import DailyCheckInRequest, DailyCheckInResponse, SleepRecordRequest, SleepRecordResponse, HabitBase, HabitResponse, LifestyleSummaryResponse
from app.api.dependencies import get_current_user
from app.services.lifestyle_engine import LifestyleEngine

router = APIRouter(prefix="/api/lifestyle", tags=["lifestyle"])

@router.post("/check-in", response_model=DailyCheckInResponse)
def create_checkin(req: DailyCheckInRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today_start = datetime.combine(date.today(), datetime.min.time())
    
    # Check if already checked in
    existing = db.query(DailyCheckIn).filter(
        DailyCheckIn.user_id == current_user.id,
        DailyCheckIn.date >= today_start
    ).first()
    
    if existing:
        existing.energy = req.energy
        existing.stress = req.stress
        existing.mood = req.mood
        existing.productivity = req.productivity
        existing.notes = req.notes
        db.commit()
        db.refresh(existing)
        return existing
        
    checkin = DailyCheckIn(
        user_id=current_user.id,
        energy=req.energy,
        stress=req.stress,
        mood=req.mood,
        productivity=req.productivity,
        notes=req.notes
    )
    db.add(checkin)
    
    # Gamification
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 15
        
    db.commit()
    db.refresh(checkin)
    return checkin

@router.get("/check-in/today", response_model=DailyCheckInResponse)
def get_today_checkin(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today_start = datetime.combine(date.today(), datetime.min.time())
    checkin = db.query(DailyCheckIn).filter(
        DailyCheckIn.user_id == current_user.id,
        DailyCheckIn.date >= today_start
    ).first()
    if not checkin:
        raise HTTPException(status_code=404, detail="No check-in today")
    return checkin
    
@router.post("/sleep", response_model=SleepRecordResponse)
def log_sleep(req: SleepRecordRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sleep = SleepRecord(
        user_id=current_user.id,
        bedtime=req.bedtime,
        wake_time=req.wake_time,
        sleep_duration=req.sleep_duration,
        sleep_quality=req.sleep_quality
    )
    db.add(sleep)
    
    # Gamification
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 15
        
    db.commit()
    db.refresh(sleep)
    return sleep

@router.get("/sleep/history", response_model=List[SleepRecordResponse])
def get_sleep_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SleepRecord).filter(SleepRecord.user_id == current_user.id).order_by(SleepRecord.date.desc()).limit(14).all()

@router.post("/habits", response_model=HabitResponse)
def create_habit(req: HabitBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    habit = Habit(
        user_id=current_user.id,
        name=req.name,
        category=req.category,
        target_frequency=req.target_frequency
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

@router.get("/habits")
def get_habits(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    habits = db.query(Habit).filter(Habit.user_id == current_user.id, Habit.is_active == True).all()
    today_start = datetime.combine(date.today(), datetime.min.time())
    
    results = []
    for h in habits:
        is_completed_today = db.query(HabitLog).filter(
            HabitLog.habit_id == h.id, 
            HabitLog.date >= today_start,
            HabitLog.completed == True
        ).first() is not None
        
        results.append({
            "id": h.id,
            "name": h.name,
            "category": h.category,
            "is_completed_today": is_completed_today
        })
    return results

@router.post("/habits/{habit_id}/complete")
def complete_habit(habit_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
        
    today_start = datetime.combine(date.today(), datetime.min.time())
    existing_log = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.date >= today_start
    ).first()
    
    if existing_log:
        existing_log.completed = True
    else:
        log = HabitLog(habit_id=habit_id, user_id=current_user.id, completed=True)
        db.add(log)
        
    # Gamification
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 5
        
    db.commit()
    return {"status": "success"}

@router.get("/summary", response_model=LifestyleSummaryResponse)
def get_lifestyle_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lifestyle_score = LifestyleEngine.calculate_lifestyle_score(db, current_user.id)
    recovery_score = LifestyleEngine.calculate_recovery_score(db, current_user.id)
    insight = LifestyleEngine.generate_insight(db, current_user.id)
    
    # Get sleep
    sleep = db.query(SleepRecord).filter(SleepRecord.user_id == current_user.id).order_by(SleepRecord.date.desc()).first()
    
    # Get Checkin
    today_start = datetime.combine(date.today(), datetime.min.time())
    checkin = db.query(DailyCheckIn).filter(
        DailyCheckIn.user_id == current_user.id,
        DailyCheckIn.date >= today_start
    ).first()
    
    # Habits
    active_habits = db.query(Habit).filter(Habit.user_id == current_user.id, Habit.is_active == True).all()
    habit_ids = [h.id for h in active_habits]
    completed_today = 0
    if habit_ids:
        completed_today = db.query(HabitLog).filter(
            HabitLog.user_id == current_user.id,
            HabitLog.habit_id.in_(habit_ids),
            HabitLog.date >= today_start,
            HabitLog.completed == True
        ).count()
    
    return LifestyleSummaryResponse(
        lifestyle_score=lifestyle_score,
        recovery_score=recovery_score,
        sleep_duration=sleep.sleep_duration if sleep else 0.0,
        active_habits_count=len(active_habits),
        completed_habits_today=completed_today,
        energy=checkin.energy if checkin else 0,
        stress=checkin.stress if checkin else 0,
        ai_insight=insight
    )
