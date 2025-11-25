from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# --- IMPORTANT: We are NOW importing ALL 3 ROUTERS ---
from .routers import data_analytics, recommendations, integrations
# --------------------------------------------------

# Load environment variables
load_dotenv()

# Initialize FastAPI App
app = FastAPI(
    title="AI Marketing Optimizer API",
    version="1.1.0", # Subimos versión por la nueva feature
    description="Backend API for marketing data analysis, AI optimization, and Webhook Integrations."
)

# --- CORS CONFIGURATION ---
origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTER ROUTERS ---

# 1. Core Analytics
app.include_router(data_analytics.router)

# 2. AI Recommendations
app.include_router(recommendations.router) 

# 3. External Integrations (Webhook para n8n/Make)
app.include_router(integrations.router)

# ---------------------------------------------------------------

# --- ROOT ENDPOINT ---
@app.get("/", tags=["General"])
def health_check():
    """Simple check to see if the server is running"""
    return {
        "status": "online",
        "system": "AI Marketing Optimizer",
        "modules": ["Analytics", "AI Agent", "Integrations"],
        "environment": os.getenv("ENV", "development")
    }