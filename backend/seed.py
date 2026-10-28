from app.db.database import SessionLocal, Base, engine
from app.models.fitness import Exercise
from app.models.nutrition import Food

# Recreate the tables
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    
    # Check if seeded
    if db.query(Exercise).first():
        print("Exercises already seeded.")
        return
        
    exercises = [
        # Beginner
        {"name": "Wall Push-up", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Chest, Triceps", "progression_level": 1},
        {"name": "Incline Push-up", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Chest, Triceps", "progression_level": 2},
        {"name": "Knee Push-up", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Chest, Triceps", "progression_level": 3},
        {"name": "Bodyweight Squat", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Quads, Glutes", "progression_level": 1},
        {"name": "Reverse Lunge", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Quads, Glutes", "progression_level": 2},
        {"name": "Glute Bridge", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Glutes", "progression_level": 1},
        {"name": "Plank", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Core", "progression_level": 1, "estimated_duration": 45},
        {"name": "Dead Bug", "difficulty": "Beginner", "exercise_type": "Strength", "muscle_groups": "Core", "progression_level": 1},
        {"name": "Bird Dog", "difficulty": "Beginner", "exercise_type": "Mobility", "muscle_groups": "Core", "progression_level": 1},
        
        # Intermediate
        {"name": "Push-up", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Chest, Triceps", "progression_level": 4},
        {"name": "Diamond Push-up", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Triceps, Chest", "progression_level": 5},
        {"name": "Pike Push-up", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Shoulders, Triceps", "progression_level": 6},
        {"name": "Pull-up", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Lats, Biceps", "equipment_required": "Pull-up bar", "progression_level": 4},
        {"name": "Chin-up", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Biceps, Lats", "equipment_required": "Pull-up bar", "progression_level": 4},
        {"name": "Dips", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Chest, Triceps", "equipment_required": "Dip bars", "progression_level": 4},
        {"name": "Bulgarian Split Squat", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Quads, Glutes", "progression_level": 4},
        {"name": "Hollow Body Hold", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Core", "progression_level": 4, "estimated_duration": 45},
        {"name": "L-Sit Progression", "difficulty": "Intermediate", "exercise_type": "Strength", "muscle_groups": "Core, Hip Flexors", "progression_level": 5, "estimated_duration": 30},

        # Advanced
        {"name": "Handstand", "difficulty": "Advanced", "exercise_type": "Strength", "muscle_groups": "Shoulders, Core", "progression_level": 7, "estimated_duration": 30},
        {"name": "Handstand Push-up Progression", "difficulty": "Advanced", "exercise_type": "Strength", "muscle_groups": "Shoulders, Triceps", "progression_level": 8},
        {"name": "Muscle-up Progression", "difficulty": "Advanced", "exercise_type": "Strength", "muscle_groups": "Back, Chest, Triceps", "equipment_required": "Pull-up bar", "progression_level": 8},
        {"name": "Front Lever Progression", "difficulty": "Advanced", "exercise_type": "Strength", "muscle_groups": "Lats, Core", "equipment_required": "Pull-up bar", "progression_level": 8},
        {"name": "Back Lever Progression", "difficulty": "Advanced", "exercise_type": "Strength", "muscle_groups": "Chest, Core", "equipment_required": "Pull-up bar", "progression_level": 8},
        {"name": "Planche Progression", "difficulty": "Advanced", "exercise_type": "Strength", "muscle_groups": "Shoulders, Core", "progression_level": 9},
        {"name": "Pistol Squat", "difficulty": "Advanced", "exercise_type": "Strength", "muscle_groups": "Quads, Glutes", "progression_level": 7}
    ]
    
    for ex_data in exercises:
        ex = Exercise(**ex_data)
        db.add(ex)
        
    db.commit()
    print("Seeded database with calisthenics exercises.")

    # 2. Seed Foods
    if db.query(Food).first():
        print("Foods already seeded.")
        return
        
    foods = [
        {"name": "Oats", "category": "Grain", "serving_size": "100g", "calories": 389, "protein": 16.9, "carbohydrates": 66.3, "fats": 6.9, "fiber": 10.6, "budget_level": "Low", "dietary_tags": "Vegan,Vegetarian,Dairy-Free"},
        {"name": "Banana", "category": "Fruit", "serving_size": "1 medium", "calories": 105, "protein": 1.3, "carbohydrates": 27, "fats": 0.3, "fiber": 3.1, "budget_level": "Low", "dietary_tags": "Vegan,Vegetarian,Dairy-Free,Gluten-Free"},
        {"name": "Milk (Whole)", "category": "Dairy", "serving_size": "1 cup", "calories": 149, "protein": 7.7, "carbohydrates": 11.7, "fats": 8.0, "fiber": 0, "budget_level": "Moderate", "dietary_tags": "Vegetarian,Gluten-Free"},
        {"name": "Rice (White)", "category": "Grain", "serving_size": "100g cooked", "calories": 130, "protein": 2.7, "carbohydrates": 28, "fats": 0.3, "fiber": 0.4, "budget_level": "Low", "dietary_tags": "Vegan,Vegetarian,Dairy-Free,Gluten-Free"},
        {"name": "Dal (Lentils)", "category": "Protein", "serving_size": "100g cooked", "calories": 116, "protein": 9.0, "carbohydrates": 20, "fats": 0.4, "fiber": 7.9, "budget_level": "Low", "dietary_tags": "Vegan,Vegetarian,Dairy-Free,Gluten-Free"},
        {"name": "Paneer", "category": "Protein", "serving_size": "100g", "calories": 296, "protein": 18.0, "carbohydrates": 1.2, "fats": 20.8, "fiber": 0, "budget_level": "Moderate", "dietary_tags": "Vegetarian,Gluten-Free"},
        {"name": "Tofu", "category": "Protein", "serving_size": "100g", "calories": 144, "protein": 15.8, "carbohydrates": 2.8, "fats": 8.7, "fiber": 2.3, "budget_level": "Moderate", "dietary_tags": "Vegan,Vegetarian,Dairy-Free,Gluten-Free"},
        {"name": "Chicken Breast", "category": "Protein", "serving_size": "100g cooked", "calories": 165, "protein": 31.0, "carbohydrates": 0, "fats": 3.6, "fiber": 0, "budget_level": "Moderate", "dietary_tags": "Dairy-Free,Gluten-Free"},
        {"name": "Eggs", "category": "Protein", "serving_size": "1 large", "calories": 72, "protein": 6.3, "carbohydrates": 0.4, "fats": 4.8, "fiber": 0, "budget_level": "Low", "dietary_tags": "Vegetarian,Dairy-Free,Gluten-Free"},
        {"name": "Peanuts", "category": "Fat", "serving_size": "30g", "calories": 170, "protein": 7.3, "carbohydrates": 4.6, "fats": 14.7, "fiber": 2.5, "budget_level": "Low", "dietary_tags": "Vegan,Vegetarian,Dairy-Free,Gluten-Free"},
        {"name": "Broccoli", "category": "Vegetable", "serving_size": "100g", "calories": 34, "protein": 2.8, "carbohydrates": 6.6, "fats": 0.4, "fiber": 2.6, "budget_level": "Moderate", "dietary_tags": "Vegan,Vegetarian,Dairy-Free,Gluten-Free"}
    ]
    
    for food_data in foods:
        f = Food(**food_data)
        db.add(f)
        
    db.commit()
    print("Seeded database with foods.")

if __name__ == "__main__":
    seed()
