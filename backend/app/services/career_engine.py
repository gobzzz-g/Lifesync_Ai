from sqlalchemy.orm import Session
from datetime import datetime, date
from app.models.user import UserProfile
from app.models.career import UserSkill, CareerGoal, Roadmap, RoadmapTask, InterviewHistory
import random

# Mock dictionary for target role requirements
ROLE_REQUIREMENTS = {
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git", "REST APIs"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Redux", "TypeScript", "Tailwind", "Git"],
    "Backend Developer": ["Python", "Node.js", "SQL", "Docker", "REST APIs", "Git", "PostgreSQL", "AWS"],
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Pandas", "Statistics", "Data Visualization"]
}

class CareerEngine:

    @staticmethod
    def analyze_skill_gap(db: Session, user_id: int):
        goal = db.query(CareerGoal).filter(CareerGoal.user_id == user_id).first()
        target_role = goal.target_role if goal else "Full Stack Developer"
        
        required_skills = ROLE_REQUIREMENTS.get(target_role, ROLE_REQUIREMENTS["Full Stack Developer"])
        user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
        
        user_skill_map = {s.name.lower(): s.proficiency_level for s in user_skills}
        
        strong = []
        improving = []
        missing = []
        
        for req in required_skills:
            req_lower = req.lower()
            if req_lower in user_skill_map:
                prof = user_skill_map[req_lower]
                if prof == "Advanced":
                    strong.append(req)
                else:
                    improving.append(req)
            else:
                missing.append(req)
                
        # Calculate readiness score (0-100)
        coverage = len(strong) + (len(improving) * 0.5)
        score = min(100, int((coverage / len(required_skills)) * 100)) if required_skills else 50
        
        return {
            "readiness_score": score,
            "strong_skills": strong,
            "improving_skills": improving,
            "missing_skills": missing,
            "priority_skills": missing[:3] # Top 3 missing are priority
        }

    @staticmethod
    def generate_roadmap(db: Session, user_id: int) -> Roadmap:
        # Delete existing roadmap
        db.query(Roadmap).filter(Roadmap.user_id == user_id).delete()
        db.commit()
        
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        target_role = "Full Stack Developer"
        base_time = 60
        
        if profile:
            if profile.career_goal or profile.target_career:
                target_role = profile.target_career or profile.career_goal
            if profile.available_learning_time and str(profile.available_learning_time).isdigit():
                base_time = int(profile.available_learning_time)
        
        # LIFESTYLE INTEGRATION: Check recovery and scale down time if tired
        from app.services.lifestyle_engine import LifestyleEngine
        recovery = LifestyleEngine.calculate_recovery_score(db, user_id)
        
        if recovery < 50:
            base_time = int(base_time * 0.5) # Cut learning time in half on low energy days
        
        roadmap = Roadmap(user_id=user_id, target_role=target_role)
        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)
        
        gap = CareerEngine.analyze_skill_gap(db, user_id)
        skills_to_learn = gap["missing_skills"] + gap["improving_skills"]
        
        if not skills_to_learn:
            skills_to_learn = ["Advanced System Design", "Algorithm Optimization", "Leadership"]
            
        tasks = []
        for i, skill in enumerate(skills_to_learn[:5]): # Generate 5 tasks
            tasks.append(RoadmapTask(
                roadmap_id=roadmap.id,
                title=f"Learn {skill} fundamentals",
                skill=skill,
                estimated_minutes=base_time
            ))
            
        db.add_all(tasks)
        db.commit()
        return roadmap

    @staticmethod
    def mock_resume_analysis(filename: str):
        # A robust mock for resume analysis
        return {
            "score": random.randint(60, 85),
            "strengths": ["Clear formatting", "Relevant experience listed"],
            "missing_skills": ["Testing", "CI/CD", "Cloud Deployment"],
            "improvement_suggestions": [
                "Add more quantifiable metrics to your bullet points (e.g. 'Improved speed by 20%').",
                "Include a link to your GitHub or portfolio.",
                "Highlight specific technologies used in your recent project."
            ]
        }

    @staticmethod
    def mock_job_analysis(job_desc: str):
        # A robust mock for Job vs Resume analysis
        return {
            "match_percentage": random.randint(55, 80),
            "matching_skills": ["JavaScript", "React", "Git"],
            "missing_skills": ["Docker", "Kubernetes", "GraphQL"],
            "recommended_improvements": [
                "The job emphasizes microservices; consider learning Docker basics.",
                "Highlight your React experience more prominently."
            ]
        }

    @staticmethod
    def mock_interview_feedback(answer: str):
        score = 0
        if len(answer) > 50: score += 40
        if "because" in answer.lower() or "example" in answer.lower(): score += 20
        if "useState" in answer or "React" in answer or "function" in answer: score += 20
        
        score = min(100, score + random.randint(0, 20)) # Cap at 100
        
        return {
            "score": score,
            "feedback": "Good attempt. You covered the basics but could elaborate more on trade-offs.",
            "strong_areas": ["Communication clarity", "Directly answering the prompt"],
            "weak_areas": ["Depth of technical explanation", "Providing concrete examples"],
            "recommended_topics": ["State management", "Performance optimization"]
        }
