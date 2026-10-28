import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LifeSync AI"
    # Provide a default secret key for development, but expect it in env in prod
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretdevelopmentkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

settings = Settings()
