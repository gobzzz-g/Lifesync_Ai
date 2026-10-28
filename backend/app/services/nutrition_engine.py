from sqlalchemy.orm import Session
from datetime import datetime, date
import random
from app.models.user import UserProfile
from app.models.nutrition import Food, MealPlan, Meal, FoodLog

class NutritionEngine:
    
    @staticmethod
    def calculate_targets(profile: UserProfile):
        """Estimate TDEE and Macro targets based on Profile."""
        weight = profile.weight or 70
        height = profile.height or 170
        age = 30 
        
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        activity_multiplier = 1.2
        productivity_val = getattr(profile, 'productivity_level', 0) or 0
        if productivity_val >= 7:
            activity_multiplier = 1.55
            
        tdee = bmr * activity_multiplier
        
        goal = profile.fitness_goal or "General Fitness"
        if "lose" in goal.lower() or "fat" in goal.lower() or "cut" in goal.lower():
            tdee -= 500
        elif "build" in goal.lower() or "gain" in goal.lower() or "bulk" in goal.lower():
            tdee += 300
            
        target_calories = max(1200, int(tdee))
        target_protein = int(weight * 2.2) 
        if "build" in goal.lower() or "muscle" in goal.lower():
            target_protein = int(weight * 2.5)
            
        remaining_cals = target_calories - (target_protein * 4)
        target_fats = max(30, int((remaining_cals * 0.3) / 9))
        target_carbs = max(50, int((remaining_cals * 0.7) / 4))
        
        return target_calories, target_protein, target_carbs, target_fats

    @staticmethod
    def get_meal_database():
        # A static database of realistic meals
        return [
            # VEGETARIAN
            {"name": "Vegetable Pongal + Sambar + Curd", "type": "Breakfast", "diet": ["Vegetarian"], "calories": 450, "protein": 15, "carbs": 65, "fats": 12, "ingredients": [{"name": "Vegetable Pongal", "amount": "1 bowl"}, {"name": "Sambar", "amount": "1 cup"}, {"name": "Curd", "amount": "1/2 cup"}]},
            {"name": "Idli + Sambar + Coconut Chutney", "type": "Breakfast", "diet": ["Vegetarian", "Vegan"], "calories": 400, "protein": 12, "carbs": 60, "fats": 10, "ingredients": [{"name": "Idli", "amount": "3 pieces"}, {"name": "Sambar", "amount": "1 cup"}, {"name": "Chutney", "amount": "2 tbsp"}]},
            {"name": "Poha with Peanuts & Veggies", "type": "Breakfast", "diet": ["Vegetarian", "Vegan"], "calories": 380, "protein": 8, "carbs": 55, "fats": 14, "ingredients": [{"name": "Poha", "amount": "1 bowl"}, {"name": "Peanuts", "amount": "30g"}]},
            {"name": "Rice + Sambar + Poriyal + Curd", "type": "Lunch", "diet": ["Vegetarian"], "calories": 650, "protein": 20, "carbs": 100, "fats": 15, "ingredients": [{"name": "Rice", "amount": "1 cup"}, {"name": "Sambar", "amount": "1 cup"}, {"name": "Veg Poriyal", "amount": "1 cup"}, {"name": "Curd", "amount": "1/2 cup"}]},
            {"name": "Quinoa Salad + Roasted Chickpeas", "type": "Lunch", "diet": ["Vegetarian", "Vegan"], "calories": 550, "protein": 22, "carbs": 70, "fats": 18, "ingredients": [{"name": "Quinoa", "amount": "1 cup"}, {"name": "Chickpeas", "amount": "100g"}]},
            {"name": "Dal Makhani + Jeera Rice + Raita", "type": "Lunch", "diet": ["Vegetarian"], "calories": 700, "protein": 25, "carbs": 95, "fats": 22, "ingredients": [{"name": "Dal", "amount": "1.5 cup"}, {"name": "Jeera Rice", "amount": "1 cup"}, {"name": "Raita", "amount": "1/2 cup"}]},
            {"name": "Chapati + Paneer Kurma + Salad", "type": "Dinner", "diet": ["Vegetarian"], "calories": 550, "protein": 25, "carbs": 60, "fats": 20, "ingredients": [{"name": "Chapati", "amount": "2 pieces"}, {"name": "Paneer Kurma", "amount": "1 cup"}, {"name": "Salad", "amount": "1 bowl"}]},
            {"name": "Tofu Stir Fry with Brown Rice", "type": "Dinner", "diet": ["Vegetarian", "Vegan"], "calories": 500, "protein": 24, "carbs": 65, "fats": 16, "ingredients": [{"name": "Tofu", "amount": "150g"}, {"name": "Brown Rice", "amount": "1/2 cup"}, {"name": "Mixed Veggies", "amount": "1 cup"}]},
            {"name": "Dal Tadka + Roti + Sabzi", "type": "Dinner", "diet": ["Vegetarian", "Vegan"], "calories": 580, "protein": 18, "carbs": 85, "fats": 15, "ingredients": [{"name": "Dal", "amount": "1 cup"}, {"name": "Roti", "amount": "3 pieces"}, {"name": "Sabzi", "amount": "1 cup"}]},
            
            # NON-VEGETARIAN
            {"name": "Omelette + Whole Wheat Toast", "type": "Breakfast", "diet": ["Non-Vegetarian"], "calories": 420, "protein": 22, "carbs": 35, "fats": 20, "ingredients": [{"name": "Eggs", "amount": "3"}, {"name": "Toast", "amount": "2 slices"}]},
            {"name": "Scrambled Eggs + Avocado + Berries", "type": "Breakfast", "diet": ["Non-Vegetarian"], "calories": 480, "protein": 24, "carbs": 25, "fats": 28, "ingredients": [{"name": "Eggs", "amount": "3"}, {"name": "Avocado", "amount": "1/2"}]},
            {"name": "Rice + Chicken Curry + Veggies", "type": "Lunch", "diet": ["Non-Vegetarian"], "calories": 700, "protein": 45, "carbs": 75, "fats": 22, "ingredients": [{"name": "Rice", "amount": "1 cup"}, {"name": "Chicken", "amount": "150g"}, {"name": "Veggies", "amount": "1 cup"}]},
            {"name": "Grilled Fish + Quinoa + Asparagus", "type": "Lunch", "diet": ["Non-Vegetarian"], "calories": 600, "protein": 42, "carbs": 50, "fats": 20, "ingredients": [{"name": "Fish", "amount": "150g"}, {"name": "Quinoa", "amount": "1 cup"}]},
            {"name": "Chapati + Chicken Tikka Masala", "type": "Dinner", "diet": ["Non-Vegetarian"], "calories": 650, "protein": 40, "carbs": 65, "fats": 25, "ingredients": [{"name": "Chapati", "amount": "2 pieces"}, {"name": "Chicken", "amount": "150g"}]},
            {"name": "Baked Salmon + Sweet Potato", "type": "Dinner", "diet": ["Non-Vegetarian"], "calories": 550, "protein": 38, "carbs": 40, "fats": 24, "ingredients": [{"name": "Salmon", "amount": "150g"}, {"name": "Sweet Potato", "amount": "1 cup"}]}
        ]

    @staticmethod
    def generate_meal_plan(db: Session, user_id: int, force_regenerate: bool = False) -> MealPlan:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)
            db.commit()
            db.refresh(profile)

        # Ensure targets are set
        if not profile.target_calories:
            cals, p, c, f = NutritionEngine.calculate_targets(profile)
            profile.target_calories = cals
            profile.target_protein = p
            profile.target_carbs = c
            profile.target_fats = f
            db.commit()

        # Check for existing plan for today
        today = datetime.combine(date.today(), datetime.min.time())
        existing_plan = db.query(MealPlan).filter(MealPlan.user_id == user_id, MealPlan.date >= today).first()
        
        if existing_plan and not force_regenerate:
            return existing_plan
            
        if existing_plan and force_regenerate:
            db.delete(existing_plan)
            db.commit()

        # Build Preference Matcher
        diet = (profile.dietary_preferences or "Anything").lower()
        if "vegan" in diet:
            req_diet = "Vegan"
        elif "vegetarian" in diet:
            req_diet = "Vegetarian"
        else:
            req_diet = "Non-Vegetarian"
            
        allergies = [a.strip().lower() for a in (profile.allergies or "").split(",")]
        avoids = [a.strip().lower() for a in (profile.foods_to_avoid or "").split(",")]
        prefs = [p.strip().lower() for p in (profile.food_preferences or "").split(",")]

        # Filter the database
        db_meals = NutritionEngine.get_meal_database()
        valid_meals = []
        for m in db_meals:
            # Check Diet
            if req_diet == "Vegan" and "Vegan" not in m["diet"]:
                continue
            if req_diet == "Vegetarian" and "Vegetarian" not in m["diet"] and "Vegan" not in m["diet"]:
                continue
                
            # Check Allergies/Avoids
            conflict = False
            for avoid in allergies + avoids:
                if avoid and avoid in m["name"].lower():
                    conflict = True
                    break
            if conflict:
                continue
                
            valid_meals.append(m)

        if not valid_meals:
            valid_meals = db_meals # Fallback if too restrictive

        # Scale macros to fit user targets
        target_cals = profile.target_calories
        target_p = profile.target_protein
        
        plan = MealPlan(
            user_id=user_id,
            total_calories=0,
            total_protein=0,
            total_carbs=0,
            total_fats=0
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)

        meal_types = [("Breakfast", 0.30), ("Lunch", 0.40), ("Dinner", 0.30)]
        for (m_type, ratio) in meal_types:
            candidates = [m for m in valid_meals if m["type"] == m_type]
            if not candidates:
                candidates = valid_meals
                
            # Seed randomization with time for regeneration
            import time
            random.seed(int(time.time() * 1000) + len(m_type))
            selected = random.choice(candidates)
            
            # Scale macros
            meal_cals = int(target_cals * ratio)
            scale_factor = meal_cals / max(1, selected["calories"])
            
            adj_cals = meal_cals
            adj_p = int(selected["protein"] * scale_factor)
            adj_c = int(selected["carbs"] * scale_factor)
            adj_f = int(selected["fats"] * scale_factor)

            # Generate AI Explanation
            explanation = f"Recommended because it fits your {req_diet.lower()} preference"
            if profile.fitness_goal:
                explanation += f" and supports your {profile.fitness_goal} goal"
            explanation += f". It provides a balanced {m_type.lower()} with roughly {adj_p}g of protein."

            meal = Meal(
                meal_plan_id=plan.id,
                name=selected["name"],
                meal_type=m_type,
                ingredients=selected["ingredients"],
                calories=adj_cals,
                protein=adj_p,
                carbohydrates=adj_c,
                fats=adj_f,
                preparation_time=15,
                ai_explanation=explanation
            )
            db.add(meal)
            
            plan.total_calories += adj_cals
            plan.total_protein += adj_p
            plan.total_carbs += adj_c
            plan.total_fats += adj_f

        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def replace_meal(db: Session, user_id: int, meal_id: int) -> MealPlan:
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal:
            raise ValueError("Meal not found")
            
        plan = db.query(MealPlan).filter(MealPlan.id == meal.meal_plan_id).first()
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        # Build Preference Matcher
        diet = (profile.dietary_preferences or "Anything").lower()
        if "vegan" in diet:
            req_diet = "Vegan"
        elif "vegetarian" in diet:
            req_diet = "Vegetarian"
        else:
            req_diet = "Non-Vegetarian"
            
        allergies = [a.strip().lower() for a in (profile.allergies or "").split(",")]
        avoids = [a.strip().lower() for a in (profile.foods_to_avoid or "").split(",")]
        
        db_meals = NutritionEngine.get_meal_database()
        candidates = []
        for m in db_meals:
            if m["type"] != meal.meal_type:
                continue
            if req_diet == "Vegan" and "Vegan" not in m["diet"]:
                continue
            if req_diet == "Vegetarian" and "Vegetarian" not in m["diet"] and "Vegan" not in m["diet"]:
                continue
            if m["name"] == meal.name:
                continue # Don't replace with same meal
                
            conflict = False
            for avoid in allergies + avoids:
                if avoid and avoid in m["name"].lower():
                    conflict = True
                    break
            if conflict:
                continue
            candidates.append(m)
            
        if not candidates:
            # Fallback
            candidates = [m for m in db_meals if m["type"] == meal.meal_type]

        import random
        selected = random.choice(candidates)
        
        # Scale to match original meal's calories
        target_cals = meal.calories
        scale_factor = target_cals / max(1, selected["calories"])
        
        adj_cals = target_cals
        adj_p = int(selected["protein"] * scale_factor)
        adj_c = int(selected["carbs"] * scale_factor)
        adj_f = int(selected["fats"] * scale_factor)
        
        # Update plan totals
        plan.total_calories = plan.total_calories - meal.calories + adj_cals
        plan.total_protein = plan.total_protein - meal.protein + adj_p
        plan.total_carbs = plan.total_carbs - meal.carbohydrates + adj_c
        plan.total_fats = plan.total_fats - meal.fats + adj_f
        
        explanation = f"Recommended because it fits your {req_diet.lower()} preference"
        if profile.fitness_goal:
            explanation += f" and supports your {profile.fitness_goal} goal"
        explanation += f". It provides a balanced {meal.meal_type.lower()} with roughly {adj_p}g of protein."
        
        # Update meal
        meal.name = selected["name"]
        meal.ingredients = selected["ingredients"]
        meal.calories = adj_cals
        meal.protein = adj_p
        meal.carbohydrates = adj_c
        meal.fats = adj_f
        meal.ai_explanation = explanation
        
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def calculate_score(db: Session, user_id: int):
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        today = datetime.combine(date.today(), datetime.min.time())
        logs = db.query(FoodLog).filter(FoodLog.user_id == user_id, FoodLog.logged_at >= today).all()
        
        if not logs or not profile.target_calories:
            return 50 # Default baseline
            
        consumed_cals = sum(log.calories for log in logs)
        cal_ratio = consumed_cals / profile.target_calories
        
        score = 100
        # Penalize if over/under eating by > 20%
        if cal_ratio > 1.2 or cal_ratio < 0.8:
            score -= 20
            
        # Water bonus
        if profile.water_consumed and profile.water_target:
            if profile.water_consumed >= profile.water_target:
                score = min(100, score + 10)
                
        return int(score)

    @staticmethod
    def mock_analyze_image():
        # A mock robust fallback if AI vision API is not present
        return {
            "food_name": random.choice(["Chicken Salad", "Oatmeal Bowl", "Avocado Toast", "Paneer Tikka"]),
            "estimated_portion": "1 serving",
            "calories": random.randint(250, 600),
            "protein": random.randint(10, 40),
            "carbohydrates": random.randint(20, 60),
            "fats": random.randint(10, 25),
            "message": "AI-generated nutritional estimates. Actual values may vary depending on ingredients and portion size."
        }
