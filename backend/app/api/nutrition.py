from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from app.db.database import get_db
from app.models.user import User, UserProfile
from app.models.nutrition import Food, MealPlan, FoodLog
from app.schemas.nutrition import FoodBase, MealPlanResponse, FoodLogRequest, FoodLogResponse, ImageAnalysisResponse, AddWaterRequest
from app.api.dependencies import get_current_user
from app.services.nutrition_engine import NutritionEngine

router = APIRouter(prefix="/api/nutrition", tags=["nutrition"])

@router.get("/foods", response_model=List[FoodBase])
def get_foods(db: Session = Depends(get_db)):
    return db.query(Food).all()

@router.get("/today", response_model=MealPlanResponse)
def get_today_meal_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today_start = datetime.combine(date.today(), datetime.min.time())
    plan = db.query(MealPlan).filter(
        MealPlan.user_id == current_user.id,
        MealPlan.date >= today_start
    ).first()
    
    if not plan:
        plan = NutritionEngine.generate_meal_plan(db, current_user.id)
        
    return plan

@router.post("/generate", response_model=MealPlanResponse)
def generate_meal_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return NutritionEngine.generate_meal_plan(db, current_user.id, force_regenerate=True)

@router.post("/replace_meal/{meal_id}", response_model=MealPlanResponse)
def replace_meal(meal_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return NutritionEngine.replace_meal(db, current_user.id, meal_id)

@router.get("/logs", response_model=List[FoodLogResponse])
def get_today_logs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today_start = datetime.combine(date.today(), datetime.min.time())
    return db.query(FoodLog).filter(
        FoodLog.user_id == current_user.id,
        FoodLog.logged_at >= today_start
    ).all()

@router.post("/log", response_model=FoodLogResponse)
def log_food(req: FoodLogRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    log = FoodLog(
        user_id=current_user.id,
        food_id=req.food_id,
        food_name=req.food_name,
        meal_type=req.meal_type,
        quantity=req.quantity,
        calories=req.calories,
        protein=req.protein,
        carbohydrates=req.carbohydrates,
        fats=req.fats,
        fiber=req.fiber
    )
    db.add(log)
    
    # Gamification: Give XP for logging
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 10
        
    db.commit()
    db.refresh(log)
    return log

@router.post("/water")
def add_water(req: AddWaterRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    profile.water_consumed = (profile.water_consumed or 0) + req.amount_ml
    profile.xp = (profile.xp or 0) + 5 # Small XP for hydration
    db.commit()
    return {"status": "success", "water_consumed": profile.water_consumed}

@router.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # Validate extension
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid image format")
        
    # In a real app, send to OpenAI Vision here
    return NutritionEngine.mock_analyze_image()

@router.get("/score")
def get_nutrition_score(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    score = NutritionEngine.calculate_score(db, current_user.id)
    return {"score": score}
