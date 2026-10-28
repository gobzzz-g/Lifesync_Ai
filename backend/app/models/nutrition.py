import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True) # E.g., Grain, Protein, Vegetable, Dairy, Fruit
    serving_size = Column(String, nullable=True) # E.g., "100g", "1 cup"
    calories = Column(Integer, default=0)
    protein = Column(Float, default=0.0) # grams
    carbohydrates = Column(Float, default=0.0) # grams
    fats = Column(Float, default=0.0) # grams
    fiber = Column(Float, default=0.0) # grams
    budget_level = Column(String, default="Moderate") # Low, Moderate, High
    dietary_tags = Column(String, nullable=True) # Comma-separated: Vegan, Vegetarian, Gluten-Free, Dairy-Free
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    total_calories = Column(Integer, default=0)
    total_protein = Column(Float, default=0.0)
    total_carbs = Column(Float, default=0.0)
    total_fats = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    meals = relationship("Meal", back_populates="plan", cascade="all, delete-orphan")

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"), nullable=False)
    name = Column(String, nullable=False) # e.g., "Breakfast"
    meal_type = Column(String, nullable=True) # e.g., "Breakfast", "Lunch", "Dinner", "Snack"
    ingredients = Column(JSON, nullable=True) # List of food names/amounts
    calories = Column(Integer, default=0)
    protein = Column(Float, default=0.0)
    carbohydrates = Column(Float, default=0.0)
    fats = Column(Float, default=0.0)
    preparation_time = Column(Integer, nullable=True) # minutes
    ai_explanation = Column(String, nullable=True)

    
    plan = relationship("MealPlan", back_populates="meals")

class FoodLog(Base):
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=True)
    food_name = Column(String, nullable=True) # If custom food
    meal_type = Column(String, nullable=True)
    quantity = Column(Float, default=1.0)
    calories = Column(Integer, default=0)
    protein = Column(Float, default=0.0)
    carbohydrates = Column(Float, default=0.0)
    fats = Column(Float, default=0.0)
    fiber = Column(Float, default=0.0)
    logged_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    food = relationship("Food")
