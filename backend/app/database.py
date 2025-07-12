from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

# Database URL configuration for Vercel
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# For Vercel deployment, use PostgreSQL if DATABASE_URL is provided
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with appropriate configuration
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database"""
    # Import models here to avoid circular imports
    from .models.user import User
    from .models.requirement import Requirement
    from .models.listing import Listing
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully") 