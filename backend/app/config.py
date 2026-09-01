import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nutrition AI Assistant"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/nutrition_ai")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Groq API
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    DIET_PLANNER_MODEL: str = os.getenv("DIET_PLANNER_MODEL", "qwen/qwen3.8-27b")
    RECOMMENDATION_MODEL: str = os.getenv("RECOMMENDATION_MODEL", "qwen/qwen3.8-27b")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
