from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from app.models.user import UserProfile
from app.models.lifestyle import SleepRecord, DailyCheckIn, Habit, HabitLog

class LifestyleEngine:

    @staticmethod
    def calculate_recovery_score(db: Session, user_id: int) -> int:
        """
        Calculates an estimated recovery indicator (0-100) using:
        - Recent sleep
        - Energy
        - Stress
        """
        today_start = datetime.combine(date.today(), datetime.min.time())
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        sleep = db.query(SleepRecord).filter(SleepRecord.user_id == user_id).order_by(SleepRecord.date.desc()).first()
        checkin = db.query(DailyCheckIn).filter(DailyCheckIn.user_id == user_id, DailyCheckIn.date >= today_start).first()
        
        score = 80 # Baseline
        
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)
            db.commit()
            db.refresh(profile)
            
        if sleep:
            # Optimal sleep ~ 7-8 hours
            if sleep.sleep_duration < 6:
                score -= 15
            elif sleep.sleep_duration > 7:
                score += 10
                
            if sleep.sleep_quality == "Poor":
                score -= 10
            elif sleep.sleep_quality == "Good":
                score += 5
                
        if checkin:
            if checkin.energy <= 4:
                score -= 10
            elif checkin.energy >= 8:
                score += 10
                
            if checkin.stress >= 7:
                score -= 15
                
        return max(0, min(100, score))

    @staticmethod
    def calculate_lifestyle_score(db: Session, user_id: int) -> int:
        """
        Holistic lifestyle score based on habit consistency, check-ins, and sleep consistency.
        """
        today_start = datetime.combine(date.today(), datetime.min.time())
        
        # Habit Completion Rate Today
        active_habits = db.query(Habit).filter(Habit.user_id == user_id, Habit.is_active == True).all()
        if not active_habits:
            return 50 # Default if no habits exist
            
        habit_ids = [h.id for h in active_habits]
        completed_logs = db.query(HabitLog).filter(
            HabitLog.user_id == user_id,
            HabitLog.habit_id.in_(habit_ids),
            HabitLog.date >= today_start,
            HabitLog.completed == True
        ).count()
        
        habit_score = (completed_logs / len(active_habits)) * 100
        
        # Recovery factors heavily into lifestyle
        recovery = LifestyleEngine.calculate_recovery_score(db, user_id)
        
        # Blended score (50% habits, 50% recovery/wellbeing)
        final_score = (habit_score * 0.5) + (recovery * 0.5)
        return int(final_score)
        
    @staticmethod
    def generate_insight(db: Session, user_id: int) -> str:
        """
        Generates a personalized insight based on recent data patterns.
        """
        last_7_days = datetime.utcnow() - timedelta(days=7)
        checkins = db.query(DailyCheckIn).filter(
            DailyCheckIn.user_id == user_id,
            DailyCheckIn.date >= last_7_days
        ).all()
        
        sleeps = db.query(SleepRecord).filter(
            SleepRecord.user_id == user_id,
            SleepRecord.date >= last_7_days
        ).all()
        
        if len(checkins) < 2 or len(sleeps) < 2:
            return "Keep tracking for a few more days to unlock personalized patterns."
            
        # Example Pattern: High productivity linked to good sleep
        avg_sleep = sum(s.sleep_duration for s in sleeps) / len(sleeps)
        avg_prod = sum(c.productivity for c in checkins) / len(checkins)
        
        if avg_sleep > 7 and avg_prod > 7:
            return "Your reported productivity appears higher on days with longer sleep."
        elif avg_sleep < 6 and avg_prod < 5:
            return "Your lower productivity appears to be associated with insufficient sleep."
            
        # Example Pattern: Stress
        avg_stress = sum(c.stress for c in checkins) / len(checkins)
        if avg_stress > 7:
            return "Your stress levels have been high recently. Consider dedicating time to recovery or mindfulness habits."
            
        return "Your lifestyle metrics are stable. Keep maintaining your healthy routines."
