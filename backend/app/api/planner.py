from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User, UserProfile
from app.models.planner import DailyPlan, DailyPlanTask, PlanFeedback
from app.api.dependencies import get_current_user
from app.schemas.planner import DailyPlanResponse, PlannerFeedbackRequest
from app.services.planner_engine import LifePlannerEngine

router = APIRouter(prefix="/api/planner", tags=["planner"])

@router.get("/today", response_model=DailyPlanResponse)
def get_today_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = LifePlannerEngine.get_today_plan(db, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="No plan found for today. Generate one.")
    return plan

@router.post("/generate", response_model=DailyPlanResponse)
def generate_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return LifePlannerEngine.generate_daily_plan(db, current_user.id)

@router.post("/tasks/{task_id}/complete")
def complete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(DailyPlanTask).filter(DailyPlanTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    plan = db.query(DailyPlan).filter(DailyPlan.id == task.daily_plan_id, DailyPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    task.is_completed = True
    
    # Award basic XP
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 10
        
    db.commit()
    return {"status": "success"}

@router.post("/feedback")
def submit_feedback(req: PlannerFeedbackRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = LifePlannerEngine.get_today_plan(db, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="No active plan to feedback on.")
        
    fb = PlanFeedback(
        user_id=current_user.id,
        daily_plan_id=plan.id,
        feeling=req.feeling,
        notes=req.notes
    )
    db.add(fb)
    db.commit()
    return {"status": "Feedback submitted successfully."}
