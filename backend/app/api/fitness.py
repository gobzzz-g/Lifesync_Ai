from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.models.fitness import Exercise, WorkoutPlan, WorkoutHistory
from app.schemas.fitness import WorkoutPlanResponse, WorkoutCompleteRequest, FitnessGenerateRequest, ExerciseBase
from app.api.dependencies import get_current_user
from app.services.fitness_engine import AdaptiveFitnessEngine
from datetime import datetime, date

router = APIRouter(prefix="/api/fitness", tags=["fitness"])

@router.get("/exercises", response_model=List[ExerciseBase])
def get_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).all()

@router.get("/today", response_model=WorkoutPlanResponse)
def get_today_workout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if there is already a workout generated for today
    today_start = datetime.combine(date.today(), datetime.min.time())
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.date >= today_start
    ).first()
    
    if not plan:
        # Generate one
        plan = AdaptiveFitnessEngine.generate_workout(db, current_user.id)
        
    return plan

@router.post("/generate", response_model=WorkoutPlanResponse)
def generate_workout(req: FitnessGenerateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Overwrite today's plan if exists
    today_start = datetime.combine(date.today(), datetime.min.time())
    db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.date >= today_start
    ).delete()
    db.commit()
    
    plan = AdaptiveFitnessEngine.generate_workout(db, current_user.id, req.available_time, req.energy, req.goal)
    return plan

@router.post("/workout/{workout_id}/complete")
def complete_workout(workout_id: int, req: WorkoutCompleteRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = AdaptiveFitnessEngine.complete_workout(db, current_user.id, workout_id, req.model_dump())
    return {"status": "success", "history_id": history.id}

@router.get("/history")
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(WorkoutHistory).filter(WorkoutHistory.user_id == current_user.id).order_by(WorkoutHistory.completed_at.desc()).all()
    return history
