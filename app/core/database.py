"""
Database configuration module.

Creates the PostgreSQL database connection and SQLAlchemy session.
Provides the get_db dependency for FastAPI route injection.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure it in your .env file.")

# SQLite requires check_same_thread=False for FastAPI
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session.

    Yields a SQLAlchemy session and ensures it is closed
    after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
