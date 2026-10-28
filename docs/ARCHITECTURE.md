# LifeSync AI Architecture

## Overview
LifeSync AI is built on a modern stack comprising a React frontend (Vite) and a FastAPI Python backend. The core innovation of the platform is its **Cross-Domain Intelligence Layer**, which treats multiple facets of a user's life (Fitness, Nutrition, Lifestyle, Career) as a single interconnected system.

## Data Flow & Engines

The architecture is driven by modular engines that feed into a central LifeState.

### 1. Domain-Specific Engines
These engines handle the deterministic and AI logic for specific areas:
- **`FitnessEngine`**: Evaluates available time and energy to generate calisthenics workouts.
- **`NutritionEngine`**: Calculates TDEE and dynamic macros based on body profile and fitness goals.
- **`LifestyleEngine`**: Tracks sleep, stress, and habits to calculate a central `recovery` score.
- **`CareerEngine`**: Analyzes skill gaps and generates learning roadmaps based on the user's target career.

### 2. The Cross-Domain Pipeline
When a user requests their dashboard or daily plan, the data flows through the following pipeline:

**Frontend Request** 
↓
**API Layer (`app/api/life.py`)**
↓
**`CrossDomainEngine`**: Aggregates the raw scores (fitness, nutrition, lifestyle, career, recovery) into a unified `LifeState` dictionary.
↓
**`LifeBalanceEngine` & `CorrelationEngine`**: Analyzes the variance between scores (penalizing extreme imbalances) and generates heuristic insights (e.g., correlating poor sleep with low energy).
↓
**`LifePlannerEngine`**: Takes the `LifeState` and the user's `available_time` budget to generate a `DailyPlan`. It utilizes a time-boxing algorithm to schedule flexible tasks, actively scaling down intensity or prioritizing recovery if the LifeState indicates burnout.
↓
**Database Storage**: The plan is saved, and user completion feeds back into Gamification (XP/Streaks).

## Database Schema (SQLite/PostgreSQL)
- **`User` / `UserProfile`**: Stores identity, biometric data, gamification state (XP, streaks, achievements).
- **Domain Tables**: `Exercise`, `WorkoutHistory`, `DailyCheckIn`, `SleepRecord`, `CareerRoadmap`.
- **Planner Tables**: `DailyPlan`, `DailyPlanTask` (tracks flexible time-blocks).

## Deployment Considerations
- **Frontend**: Single Page Application (SPA). Any routing beyond `/` should fallback to `index.html` in production.
- **Backend**: Stateless REST API. Runs via Uvicorn (`uvicorn app.main:app`). Requires `DATABASE_URL`, `JWT_SECRET_KEY`, and `ALLOWED_ORIGINS` to be injected via environment variables.
