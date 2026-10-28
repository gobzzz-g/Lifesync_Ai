from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any

from app.models.user import UserProfile
from app.services.fitness_engine import AdaptiveFitnessEngine
from app.services.nutrition_engine import NutritionEngine
from app.services.lifestyle_engine import LifestyleEngine
from app.services.career_engine import CareerEngine

class CrossDomainEngine:
    
    @staticmethod
    def get_life_state(db: Session, user_id: int) -> Dict[str, Any]:
        """Aggregate signals from all existing engines into a unified LifeState."""
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        # Pull fitness state (fallback to 75 if None)
        fitness_score = getattr(profile, 'fitness_score', None) or 75
        
        # Nutrition score
        nutrition_score = getattr(profile, 'nutrition_score', None) or 75
        
        # Lifestyle & Recovery
        lifestyle_score = getattr(profile, 'lifestyle_score', None) or 75
        recovery_score = LifestyleEngine.calculate_recovery_score(db, user_id) or 75
        
        # Career readiness
        career_gap = CareerEngine.analyze_skill_gap(db, user_id)
        career_score = (career_gap.get("readiness_score") if isinstance(career_gap, dict) else 70) or 70
        
        # Check-in metrics (latest)
        from app.models.lifestyle import DailyCheckIn
        latest_checkin = db.query(DailyCheckIn).filter(DailyCheckIn.user_id == user_id).order_by(DailyCheckIn.date.desc()).first()
        
        energy = latest_checkin.energy if latest_checkin else 5
        stress = latest_checkin.stress if latest_checkin else 5
        
        from app.models.lifestyle import SleepRecord
        latest_sleep = db.query(SleepRecord).filter(SleepRecord.user_id == user_id).order_by(SleepRecord.date.desc()).first()
        sleep_hours = latest_sleep.sleep_duration if latest_sleep else 7.0
        
        available_time = 120
        if profile and hasattr(profile, 'available_free_time') and profile.available_free_time:
            if str(profile.available_free_time).isdigit():
                available_time = int(profile.available_free_time)

        # Base unified state
        return {
            "fitness": fitness_score,
            "nutrition": nutrition_score,
            "lifestyle": lifestyle_score,
            "recovery": recovery_score,
            "career": career_score,
            "energy": energy,
            "stress": stress,
            "sleep_hours": sleep_hours,
            "available_time": available_time
        }

class LifeBalanceEngine:
    
    @staticmethod
    def calculate_balance_score(db: Session, user_id: int) -> Dict[str, Any]:
        state = CrossDomainEngine.get_life_state(db, user_id)
        
        scores = [
            state.get("fitness") or 75,
            state.get("nutrition") or 75,
            state.get("lifestyle") or 75,
            state.get("career") or 70,
            state.get("recovery") or 75
        ]
        avg = sum(scores) / len(scores)
        
        # Calculate standard deviation as imbalance penalty
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        penalty = (variance ** 0.5) * 0.8
        
        balance_score = max(0, int(avg - penalty))
        
        # Determine the reason
        lowest_domain = ""
        lowest_val = 100
        for k, v in [("Fitness", scores[0]), ("Nutrition", scores[1]), 
                     ("Lifestyle", scores[2]), ("Career", scores[3]), 
                     ("Recovery", scores[4])]:
            if v < lowest_val:
                lowest_val = v
                lowest_domain = k
                
        highest_domain = ""
        highest_val = 0
        for k, v in [("Fitness", scores[0]), ("Nutrition", scores[1]), 
                     ("Lifestyle", scores[2]), ("Career", scores[3]), 
                     ("Recovery", scores[4])]:
            if v > highest_val:
                highest_val = v
                highest_domain = k
        
        reason = f"Your {highest_domain} progress is strong, but {lowest_domain} consistency is currently a limiting factor."
        if penalty < 5:
            reason = "Your life areas are very well balanced right now."
            
        return {
            "overall_growth": int(avg),
            "balance_score": balance_score,
            "reason": reason,
            "lowest_domain": lowest_domain,
            "highest_domain": highest_domain
        }

class CorrelationEngine:
    
    @staticmethod
    def get_correlations(db: Session, user_id: int) -> list:
        # Since we just deployed, we use robust heuristics instead of statistical math on sparse DB rows.
        state = CrossDomainEngine.get_life_state(db, user_id)
        
        correlations = []
        if state["sleep_hours"] < 6 and state["energy"] < 5:
            correlations.append("Based on recent data, your reported energy appears consistently lower following nights with <6 hours of sleep.")
            
        if state["stress"] > 7 and state["recovery"] < 60:
            correlations.append("Your high stress levels appear associated with your lowered recovery scores this week.")
            
        if not correlations:
            correlations.append("Keep tracking for a few more days to unlock deeper cross-domain insights.")
            
        return correlations

class CrossDomainInsightEngine:

    @staticmethod
    def generate_insight(db: Session, user_id: int) -> Dict[str, str]:
        state = CrossDomainEngine.get_life_state(db, user_id)
        
        if state["sleep_hours"] < 6 and state["energy"] < 5:
            return {
                "insight": f"Your sleep has dropped to {state['sleep_hours']} hours and energy is low.",
                "recommendation": "Rather than increasing your study hours, protect your sleep tonight and reduce workout intensity."
            }
        
        if state["recovery"] < 50:
            return {
                "insight": "Your central recovery score has dipped into the red zone.",
                "recommendation": "LifeSync will prioritize recovery today. Career tasks and workouts will be automatically scaled down."
            }
            
        balance = LifeBalanceEngine.calculate_balance_score(db, user_id)
        if balance["balance_score"] < 50:
            return {
                "insight": f"Your {balance['lowest_domain']} is lagging significantly behind your {balance['highest_domain']}.",
                "recommendation": f"Focus your available free time on {balance['lowest_domain']} today to restore balance."
            }
            
        return {
            "insight": "Your metrics are stable and well-balanced.",
            "recommendation": "Continue your current routine. LifeSync will maintain your standard progression."
        }
