from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import UserProfile
from app.models.fitness import Exercise, WorkoutPlan, WorkoutExercise, WorkoutHistory

class AdaptiveFitnessEngine:
    
    @staticmethod
    def generate_workout(db: Session, user_id: int, available_time: int = None, energy: int = None, goal: str = None) -> WorkoutPlan:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)
            db.commit()
            db.refresh(profile)
        # 1. Read Global Profile & Preferences
        time_minutes = available_time if available_time else int(profile.available_workout_time or 30)
        energy_level = energy if energy else (profile.energy_level or 5)
        user_goal = goal if goal else (profile.fitness_goal or "General Fitness")
        difficulty_preference = profile.fitness_level or "Beginner"
        
        # Determine Recovery via Lifestyle Engine
        from app.services.lifestyle_engine import LifestyleEngine
        recovery_level = LifestyleEngine.calculate_recovery_score(db, user_id)
        
        # 2. Dynamic Adaptation based on state
        reason_parts = []
        reason_parts.append(f"✓ {time_minutes} minutes available")
        if energy_level <= 3 or recovery_level < 50:
            difficulty = "Beginner"  # Scale down
            time_minutes = min(time_minutes, 20) # Condensed for active recovery
            focus_type = "Mobility"
            reason_parts.append(f"⚠ Low energy ({energy_level}/10)")
            reason_parts.append(f"⚠ Low recovery ({recovery_level}%)")
            reason_summary = "Reduced intensity, shorter duration, and mobility focus."
        elif energy_level >= 8 and recovery_level > 80:
            difficulty = difficulty_preference
            time_minutes = min(time_minutes, 60)
            focus_type = "Strength" if "Strength" in user_goal else "Balance"
            reason_parts.append(f"✓ High energy ({energy_level}/10)")
            reason_parts.append(f"✓ Good recovery ({recovery_level}%)")
            reason_summary = "Normal/high intensity, skill progression, and strength focus."
        else:
            difficulty = difficulty_preference
            focus_type = "Strength"
            reason_parts.append(f"✓ Moderate energy ({energy_level}/10)")
            reason_parts.append(f"✓ Normal recovery ({recovery_level}%)")
            reason_summary = "Normal intensity and standard progression."
            
        reasoning_str = "Your workout was adjusted because:\n" + "\n".join(reason_parts) + f"\n\nTherefore:\n{reason_summary}"
            
        # 3. Select Exercises intelligently (Balance Push, Pull, Core/Balance)
        exercises = []
        
        if focus_type == "Mobility":
            # Just grab mobility/balance
            mob_exercises = db.query(Exercise).filter(Exercise.exercise_type.in_(["Mobility", "Balance"])).limit(4).all()
            exercises.extend(mob_exercises)
        else:
            # We want a Push, a Pull, and a Dip or Core/Balance
            push_ex = db.query(Exercise).filter(
                Exercise.difficulty == difficulty, 
                Exercise.muscle_groups.like("%Chest%")
            ).order_by(Exercise.progression_level.desc()).first()
            
            pull_ex = db.query(Exercise).filter(
                Exercise.difficulty == difficulty, 
                Exercise.muscle_groups.like("%Back%")
            ).order_by(Exercise.progression_level.desc()).first()
            
            balance_ex = db.query(Exercise).filter(
                Exercise.exercise_type == "Balance"
            ).first()
            
            # Fallbacks if none found
            if not push_ex: push_ex = db.query(Exercise).filter(Exercise.muscle_groups.like("%Chest%")).first()
            if not pull_ex: pull_ex = db.query(Exercise).filter(Exercise.muscle_groups.like("%Back%")).first()
            if not balance_ex: balance_ex = db.query(Exercise).first()
            
            if push_ex: exercises.append(push_ex)
            if pull_ex: exercises.append(pull_ex)
            if balance_ex: exercises.append(balance_ex)
            
        # 4. Create Plan
        plan = WorkoutPlan(
            user_id=user_id,
            duration=time_minutes,
            difficulty=difficulty,
            goal=user_goal,
            recovery_level=recovery_level,
            reasoning=reasoning_str
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        
        # 5. Create Workout Exercises
        order = 1
        estimated_total_time = 0
        
        for ex in exercises:
            if estimated_total_time >= (time_minutes * 60) and order > 2:
                break
                
            sets = 3
            reps = 10 if not (ex.exercise_type == "Balance") else 0
            duration = ex.estimated_duration if ex.exercise_type == "Balance" else None
            rest = 60
            
            if energy_level <= 3:
                sets = 2
                reps = max(5, reps - 2) if reps else 0
                rest = 90
            elif energy_level >= 8 and difficulty == "Advanced":
                sets = 4
                reps = reps + 2 if reps else 0
                rest = 45
                
            if time_minutes <= 20:
                sets = 2
                rest = 30
                
            we = WorkoutExercise(
                workout_id=plan.id,
                exercise_id=ex.id,
                sets=sets,
                reps=reps,
                duration=duration,
                rest_time=rest,
                difficulty=ex.difficulty,
                order=order
            )
            db.add(we)
            order += 1
            estimated_total_time += (sets * (ex.estimated_duration or 45)) + (sets * rest)
            
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def complete_workout(db: Session, user_id: int, workout_id: int, data: dict):
        history = WorkoutHistory(
            user_id=user_id,
            workout_id=workout_id,
            completion_percentage=data.get('completion_percentage', 100),
            actual_duration=data.get('actual_duration', 0),
            user_rating=data.get('user_rating', 5),
            energy_before=data.get('energy_before', 5),
            energy_after=data.get('energy_after', 5),
            notes=data.get('notes', "")
        )
        db.add(history)
        
        # Gamification update
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if profile:
            profile.xp = (profile.xp or 0) + (100 * (data.get('completion_percentage', 100) / 100))
            profile.xp = (profile.xp or 0) + 50
            profile.streak_days = (profile.streak_days or 0) + 1
            if profile.streak_days > (profile.best_streak or 0):
                profile.best_streak = profile.streak_days
            profile.last_active_date = datetime.utcnow()
            
        db.commit()
        return history
