"""
Database connection and session management for Site-Steward.
Provides SQLAlchemy engine, session factory, and base model class.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from contextlib import contextmanager
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.config import get_config

# Get configuration
config = get_config()

# Create database engine with connection pooling
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    echo=config.DEBUG,
    **config.SQLALCHEMY_ENGINE_OPTIONS
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create thread-safe scoped session
ScopedSession = scoped_session(SessionLocal)

# Create declarative base for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    
    Usage:
        with get_db() as db:
            # Use db session
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions.
    Automatically commits on success and rolls back on error.
    
    Usage:
        with get_db_context() as db:
            # Use db session
            db.add(obj)
            # Automatically commits on exit
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    Should be called once during application setup.
    """
    # Import all models to ensure they're registered with Base
    from database.models import (
        UserORM, ProjectORM, AssetORM, SubcontractorORM,
        ComplianceDocumentORM, AssetHistoryORM, PlaceORM,
        project_subcontractors
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all database tables.
    WARNING: This will delete all data!
    Should only be used in development/testing.
    """
    Base.metadata.drop_all(bind=engine)


def reset_db():
    """
    Reset the database by dropping and recreating all tables.
    WARNING: This will delete all data!
    Should only be used in development/testing.
    """
    drop_db()
    init_db()