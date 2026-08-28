import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve absolute path to .env file at the project root
ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Petrocast Resilience V2"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres"

    # Ingestion
    MARKET_POLL_INTERVAL_MINUTES: int = 15
    STALE_DATA_THRESHOLD_MINUTES: int = 15

    # Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.6-flash"

    model_config = SettingsConfigDict(env_file=str(ENV_FILE_PATH), extra="ignore")
    
settings = Settings()

