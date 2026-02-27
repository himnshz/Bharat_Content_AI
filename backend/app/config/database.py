from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - supports PostgreSQL, MySQL, SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./bharat_content_ai.db"  # Default to SQLite for development
)

# For production with AWS RDS PostgreSQL:
# DATABASE_URL = "postgresql://username:password@rds-endpoint:5432/dbname"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database tables
def init_db():
    """Create all tables in the database"""
    from app.models import (
        User, Content, Post, Translation, 
        SocialAccount, Analytics, ContentPerformance,
        VoiceInput, AIModelConfig, ModelUsageLog
    )
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")


# Drop all tables (use with caution!)
def drop_db():
    """Drop all tables from the database"""
    Base.metadata.drop_all(bind=engine)
    print("✓ Database tables dropped!")
