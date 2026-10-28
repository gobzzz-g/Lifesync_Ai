from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User, UserProfile
from app.schemas.user import ProfileResponse, ProfileUpdate
from app.api.dependencies import get_current_user
from app.services.ai_engine import PersonalProfileEngine

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("", response_model=ProfileResponse)
@router.get("/", response_model=ProfileResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    # Dynamically update AI priorities
    from app.services.ai_engine import PriorityEngine
    dynamic_priorities = PriorityEngine.generate_dynamic_priorities(db, current_user.id)
    profile.ai_priorities = dynamic_priorities
    db.commit()
    db.refresh(profile)
    
    return profile

@router.put("", response_model=ProfileResponse)
@router.put("/", response_model=ProfileResponse)
def update_profile(profile_data: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
        
    # Recalculate scores if profile changes
    current_data = {c.name: getattr(profile, c.name) for c in profile.__table__.columns}
    ai_results = PersonalProfileEngine.analyze_profile(current_data)
    for key, value in ai_results.items():
        setattr(profile, key, value)
        
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/onboarding", response_model=ProfileResponse)
def complete_onboarding(profile_data: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        
    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
        
    profile.onboarding_completed = True
    
    # Generate AI Profile
    current_data = {c.name: getattr(profile, c.name) for c in profile.__table__.columns}
    ai_results = PersonalProfileEngine.analyze_profile(current_data)
    
    for key, value in ai_results.items():
        setattr(profile, key, value)
        
    db.commit()
    db.refresh(profile)
    return profile

