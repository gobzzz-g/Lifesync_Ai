from sqlalchemy.orm import Session
from datetime import datetime, date
from app.models.planner import DailyPlan, DailyPlanTask
from app.services.cross_domain_engine import CrossDomainEngine

class LifePlannerEngine:
    
    @staticmethod
    def generate_daily_plan(db: Session, user_id: int) -> DailyPlan:
        # Delete existing plan for today to regenerate
        today = date.today()
        existing = db.query(DailyPlan).filter(DailyPlan.user_id == user_id).all()
        for p in existing:
            if p.date.date() == today:
                db.delete(p)
        db.commit()

        state = CrossDomainEngine.get_life_state(db, user_id)
        
        # Priority mapping based on state
        overall_priority = "Balanced"
        if state["recovery"] < 50 or state["energy"] < 4:
            overall_priority = "Recovery"
        elif state["career"] < 60:
            overall_priority = "Career"
        elif state["fitness"] < 60:
            overall_priority = "Fitness"
            
        plan = DailyPlan(
            user_id=user_id,
            energy_level=state["energy"],
            available_time=state["available_time"],
            overall_priority=overall_priority
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        
        # Generate Tasks (Flexible Blocks)
        tasks = []
        time_budget = state["available_time"] # e.g. 120 minutes
        
        # 1. Recovery block (Always first if needed)
        if overall_priority == "Recovery":
            tasks.append(DailyPlanTask(
                daily_plan_id=plan.id, title="Active Recovery / Light Walk", category="Lifestyle",
                duration=20, priority="High", source_module="CrossDomain", flexible=True
            ))
            time_budget -= 20
            
        # 2. Fitness Block
        workout_dur = 45 if state["energy"] >= 5 else 20
        if time_budget >= workout_dur:
            tasks.append(DailyPlanTask(
                daily_plan_id=plan.id, title="Daily Workout", category="Fitness",
                duration=workout_dur, priority="High", source_module="Fitness", flexible=True
            ))
            time_budget -= workout_dur
            
        # 3. Career Block
        if time_budget >= 30:
            career_dur = 45 if time_budget >= 45 and state["energy"] >= 5 else 30
            tasks.append(DailyPlanTask(
                daily_plan_id=plan.id, title="Career Roadmap Task", category="Career",
                duration=career_dur, priority="High", source_module="Career", flexible=True
            ))
            time_budget -= career_dur
            
        # 4. Habit / Lifestyle
        if time_budget >= 15:
            tasks.append(DailyPlanTask(
                daily_plan_id=plan.id, title="Daily Habits & Reflection", category="Lifestyle",
                duration=15, priority="Medium", source_module="Lifestyle", flexible=True
            ))
            time_budget -= 15

        # If user is totally out of time budget but needs more tasks, we don't schedule them (Time Budgeting constraint)

        db.add_all(tasks)
        db.commit()
        
        return plan

    @staticmethod
    def get_today_plan(db: Session, user_id: int):
        today = date.today()
        plans = db.query(DailyPlan).filter(DailyPlan.user_id == user_id).all()
        for p in plans:
            if p.date.date() == today:
                return p
        return None
