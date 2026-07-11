"""Configuration settings for BankShield AI"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME: str = "BankShield AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./bankshield.db"
    )
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # ML Models
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models")
    TRAIN_TEST_SPLIT: float = float(os.getenv("TRAIN_TEST_SPLIT", 0.2))
    RIPITATION_THRESHOLD: float = float(
        os.getenv("RIPITATION_THRESHOLD", 0.7)
    )

settings = Settings()
