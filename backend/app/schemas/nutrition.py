from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class FoodBase(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    serving_size: Optional[str] = None
    calories: int
    protein: float
    carbohydrates: float
    fats: float
    fiber: float
    budget_level: str
    dietary_tags: Optional[str] = None

    class Config:
        from_attributes = True

class MealResponse(BaseModel):
    id: int
    name: str
    meal_type: str
    ingredients: Any # JSON
    calories: int
    protein: float
    carbohydrates: float
    fats: float
    preparation_time: Optional[int] = None
    ai_explanation: Optional[str] = None

    class Config:
        from_attributes = True

class MealPlanResponse(BaseModel):
    id: int
    date: datetime
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fats: float
    meals: List[MealResponse] = []

    class Config:
        from_attributes = True

class FoodLogRequest(BaseModel):
    food_id: Optional[int] = None
    food_name: Optional[str] = None
    meal_type: str
    quantity: float
    calories: int
    protein: float
    carbohydrates: float
    fats: float
    fiber: float

class FoodLogResponse(BaseModel):
    id: int
    food_name: Optional[str] = None
    meal_type: str
    quantity: float
    calories: int
    protein: float
    carbohydrates: float
    fats: float
    fiber: float
    logged_at: datetime
    food: Optional[FoodBase] = None

    class Config:
        from_attributes = True

class IngredientMealRequest(BaseModel):
    ingredients: List[str]

class ImageAnalysisResponse(BaseModel):
    food_name: str
    estimated_portion: str
    calories: int
    protein: float
    carbohydrates: float
    fats: float
    message: str = "AI-generated nutritional estimates. Actual values may vary depending on ingredients and portion size."

class AddWaterRequest(BaseModel):
    amount_ml: int
