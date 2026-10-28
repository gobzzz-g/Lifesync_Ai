# LifeSync AI

## Your Personal AI Life Optimization Platform

### Overview
LifeSync AI is a comprehensive, AI-powered personal life optimization platform. Unlike standard tracking apps that isolate your health, productivity, and habits into silos, LifeSync AI acts as a **centralized intelligence layer** that understands your life as a connected system.

### Problem Statement
Most people struggle to balance their goals. When work stress increases, fitness and sleep often suffer. Standard apps don't recognize these relationships, leading to rigid plans that result in burnout.

### Solution & Core USP
**Cross-Domain Adaptive Intelligence.**
LifeSync AI continuously analyzes your **Fitness**, **Nutrition**, **Lifestyle** (Sleep/Stress), and **Career** goals to generate **one adaptive daily plan**. 
If you log poor sleep and high stress, the AI automatically reduces your generated workout intensity and scales down your career study time to prioritize recovery, keeping you balanced and preventing burnout.

### Key Features
- **Adaptive Fitness Engine**: Generates personalized calisthenics workouts that scale up or down based on your daily energy.
- **AI Nutrition Intelligence**: Dynamic macro calculation, food logging, and hydration tracking.
- **Lifestyle & Recovery**: Sleep tracking, daily check-ins, and a central Recovery Score calculation.
- **AI Career Coach**: Skill-gap analysis, dynamic learning roadmaps, resume analysis, and mock interviews.
- **Cross-Domain AI & Daily Planner**: The central engine that aggregates your 'LifeState' to intelligently time-box your day.
- **Gamification 2.0**: Global XP, leveled progression, achievements, and cross-domain streaks.

### Technology Stack
- **Frontend**: React (Vite), TypeScript, TailwindCSS, Recharts, React Router
- **Backend**: Python, FastAPI, SQLAlchemy, SQLite (Development)
- **Authentication**: JWT & bcrypt

### Installation & Running Locally

**1. Clone the repository:**
```bash
git clone <repository_url>
cd LifeSyncAI
```

**2. Start the Backend:**
```bash
cd backend
python -m venv venv
# Activate venv (Windows: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python seed.py # Initializes the database
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**3. Start the Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Security & Privacy
- Full JWT-based authentication.
- All user requests are isolated at the database query layer.
- Resume/document uploads are temporarily stored in memory for analysis and immediately discarded.

### Future Enhancements
- Integration with external LLM APIs (OpenAI) for deeper natural language processing and dynamic resume/job matching.
- Wearable device integration (Apple Health, Garmin) to automate sleep and activity tracking.
