import json

class GrowthScoreEngine:
    @staticmethod
    def calculate_scores(profile_data: dict) -> dict:
        # Simple rule-based calculation for scores
        fitness = 50
        if profile_data.get('fitness_level') == 'Beginner':
            fitness = 40
        elif profile_data.get('fitness_level') == 'Intermediate':
            fitness = 60
        elif profile_data.get('fitness_level') == 'Advanced':
            fitness = 80
            
        nutrition = 50
        if profile_data.get('meals_per_day') and profile_data['meals_per_day'] >= 3:
            nutrition += 10
            
        lifestyle = 50
        sleep = profile_data.get('sleep_duration')
        if sleep:
            if 7 <= sleep <= 9:
                lifestyle += 20
            elif sleep < 6:
                lifestyle -= 10
                
        well_being = 50
        stress = profile_data.get('stress_level')
        if stress:
            if stress < 4: well_being += 20
            elif stress > 7: well_being -= 20
            
        career = 50
        if profile_data.get('career_experience_level') == 'Advanced':
            career += 20
        elif profile_data.get('career_experience_level') == 'Intermediate':
            career += 10
            
        overall = int((fitness + nutrition + lifestyle + well_being + career) / 5)
        
        return {
            'fitness_score': max(0, min(100, fitness)),
            'nutrition_score': max(0, min(100, nutrition)),
            'lifestyle_score': max(0, min(100, lifestyle)),
            'well_being_score': max(0, min(100, well_being)),
            'career_score': max(0, min(100, career)),
            'overall_score': max(0, min(100, overall))
        }

class InsightEngine:
    @staticmethod
    def generate_insights(profile_data: dict) -> str:
        insights = []
        
        # Fitness Insight
        time = profile_data.get('available_workout_time', '30 minutes')
        insights.append(f"You have {time} available for workouts, so LifeSync will prioritize efficient routines.")
        
        # Career Insight
        career = profile_data.get('target_career')
        if career:
            insights.append(f"Your target is {career}. We will focus your roadmap on relevant practical skills.")
            
        # Lifestyle Insight
        sleep = profile_data.get('sleep_duration')
        if sleep and sleep < 7:
            insights.append("Your reported sleep duration is below optimal. Lifestyle recommendations will prioritize recovery.")
        else:
            insights.append("Your sleep schedule looks solid. Maintain this to optimize both recovery and productivity.")
            
        return json.dumps(insights)

class PriorityEngine:
    @staticmethod
    def generate_priorities(profile_data: dict) -> str:
        priorities = []
        sleep = profile_data.get('sleep_duration')
        if sleep is None:
            sleep = 7
        if float(sleep) < 7: priorities.append("🔴 Sleep & Recovery")
        else: priorities.append("🟢 Sleep Maintained")
        priorities.append("🟡 Hydration")
        if profile_data.get('career_status') == 'Job seeker': priorities.append("🔴 Career Learning")
        else: priorities.append("🟢 Career Learning")
        priorities.append("🟢 Fitness")
        return json.dumps(priorities)

    @staticmethod
    def generate_dynamic_priorities(db, user_id: int) -> str:
        from app.models.user import UserProfile
        from app.models.lifestyle import SleepRecord
        from app.models.nutrition import FoodLog
        from datetime import datetime, date

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile: return "[]"

        priorities = []
        today_start = datetime.combine(date.today(), datetime.min.time())

        # Check sleep
        sleep = db.query(SleepRecord).filter(SleepRecord.user_id == user_id).order_by(SleepRecord.date.desc()).first()
        if sleep and sleep.sleep_duration < 6:
            priorities.append("🔴 Recovery")
        else:
            priorities.append("🟢 Recovery")

        # Check hydration
        if profile.water_consumed and profile.water_target and profile.water_consumed < (profile.water_target * 0.5):
            priorities.append("🟡 Hydration")
        else:
            priorities.append("🟢 Hydration")

        # Check career
        if profile.career_status == 'Job seeker':
            priorities.append("🔴 Career")
        else:
            priorities.append("🟡 Career")

        return json.dumps(priorities)

class PersonalProfileEngine:
    @staticmethod
    def analyze_profile(profile_data: dict) -> dict:
        scores = GrowthScoreEngine.calculate_scores(profile_data)
        insights = InsightEngine.generate_insights(profile_data)
        priorities = PriorityEngine.generate_priorities(profile_data)
        
        return {
            **scores,
            'ai_insights': insights,
            'ai_priorities': priorities
        }
