"""
Database configuration and session management
"""

from sqlalchemy import create_engine, text
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
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    try:
        from app.models.user import User
        from app.models.requirement import Requirement
        from app.models.listing import Listing
        Base.metadata.create_all(bind=engine)
        # Print all table names for debug
        with engine.connect() as conn:
            table_names = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
            print(f"✅ Database tables created: {[name[0] for name in table_names]}")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise 