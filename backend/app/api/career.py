from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.models.user import User, UserProfile
from app.models.career import UserSkill, CareerGoal, Roadmap, RoadmapTask, InterviewHistory
from app.schemas.career import (
    SkillBase, UserSkillResponse, CareerGoalRequest, CareerGoalResponse, 
    RoadmapResponse, CareerGapAnalysisResponse, ResumeAnalysisResponse,
    JobAnalysisRequest, JobAnalysisResponse, MockInterviewRequest,
    MockInterviewResponse, MockInterviewAnswer, MockInterviewFeedback, InterviewHistoryResponse
)
from app.api.dependencies import get_current_user
from app.services.career_engine import CareerEngine
import random

router = APIRouter(prefix="/api/career", tags=["career"])

@router.get("/skills", response_model=List[UserSkillResponse])
def get_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()

@router.post("/skills", response_model=UserSkillResponse)
def add_skill(req: SkillBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(UserSkill).filter(UserSkill.user_id == current_user.id, UserSkill.name == req.name).first()
    if existing:
        existing.proficiency_level = req.proficiency_level
        db.commit()
        db.refresh(existing)
        return existing
        
    skill = UserSkill(user_id=current_user.id, name=req.name, proficiency_level=req.proficiency_level)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

@router.post("/analyze-gap", response_model=CareerGapAnalysisResponse)
def analyze_gap(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return CareerEngine.analyze_skill_gap(db, current_user.id)

@router.post("/roadmap/generate", response_model=RoadmapResponse)
def generate_roadmap(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return CareerEngine.generate_roadmap(db, current_user.id)

@router.get("/roadmap", response_model=RoadmapResponse)
def get_roadmap(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == current_user.id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found. Generate one first.")
    return roadmap

@router.put("/tasks/{task_id}/complete")
def complete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(RoadmapTask).filter(RoadmapTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Security check: ensure task belongs to user's roadmap
    roadmap = db.query(Roadmap).filter(Roadmap.id == task.roadmap_id, Roadmap.user_id == current_user.id).first()
    if not roadmap:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    task.is_completed = True
    task.completed_at = datetime.utcnow()
    
    # Gamification XP
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 20
        
    db.commit()
    return {"status": "success"}

@router.post("/resume/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDF and DOCX accepted.")
        
    # In a real app, parse file bytes here and send to LLM
    content = await file.read()
    # file is discarded from memory after route finishes
    
    return CareerEngine.mock_resume_analysis(file.filename)

@router.post("/job/analyze", response_model=JobAnalysisResponse)
def analyze_job(req: JobAnalysisRequest, current_user: User = Depends(get_current_user)):
    return CareerEngine.mock_job_analysis(req.job_description)

@router.post("/interview/start", response_model=MockInterviewResponse)
def start_interview(req: MockInterviewRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Record history
    history = InterviewHistory(
        user_id=current_user.id,
        role=req.role,
        interview_type=req.interview_type
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    
    questions = [
        "Tell me about a time you solved a difficult technical problem.",
        "How do you handle disagreements with a team member?",
        "Explain how REST APIs work.",
        "What is your greatest technical strength and why?"
    ]
    
    return MockInterviewResponse(id=history.id, question=random.choice(questions))

@router.post("/interview/{interview_id}/answer", response_model=MockInterviewFeedback)
def answer_interview(interview_id: int, req: MockInterviewAnswer, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(InterviewHistory).filter(InterviewHistory.id == interview_id, InterviewHistory.user_id == current_user.id).first()
    if not history:
        raise HTTPException(status_code=404, detail="Interview not found")
        
    feedback = CareerEngine.mock_interview_feedback(req.answer)
    history.score = feedback["score"]
    history.feedback = feedback["feedback"]
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 50 # Big XP for interview practice
        
    db.commit()
    return feedback

@router.get("/interviews", response_model=List[InterviewHistoryResponse])
def get_interviews(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(InterviewHistory).filter(InterviewHistory.user_id == current_user.id).order_by(InterviewHistory.date.desc()).all()
