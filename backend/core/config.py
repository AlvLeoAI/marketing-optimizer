import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Centralized configuration management.
    """
    PROJECT_NAME: str = "AI Marketing Optimizer"
    VERSION: str = "1.0.0"
    ENV: str = os.getenv("ENV", "development")
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "*"
    ]

# Instantiate settings to be imported elsewhere
settings = Settings()