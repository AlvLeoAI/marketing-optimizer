from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# --- DATABASE CONFIGURATION ---
# By default, we use SQLite (a local file) for development.
# In production, this would be changed to a PostgreSQL URL (e.g., Supabase/AWS).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketing_data.db")

# Create the database engine
# connect_args={"check_same_thread": False} is only needed for SQLite
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create the local session factory (the "connection" used in each request)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models (tables)
Base = declarative_base()

# --- DEPENDENCY (Dependency Injection) ---
# This function is used in endpoints to get a secure database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()