import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api import auth, profile, fitness, nutrition, lifestyle, career, life, planner
import app.models.user
import app.models.fitness
import app.models.nutrition
import app.models.lifestyle
import app.models.career
import app.models.planner

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LifeSync AI API", description="Backend for LifeSync AI", version="1.0.0")

# Set up CORS for frontend communication
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins = env_origins.split(",")
else:
    origins = [
        "http://localhost:5173", # Vite default port
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(fitness.router)
app.include_router(nutrition.router)
app.include_router(lifestyle.router)
app.include_router(career.router)
app.include_router(life.router)
app.include_router(planner.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to LifeSync AI API"}
