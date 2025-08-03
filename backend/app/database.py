"""Database configuration for the FastAPI application.

This module sets up a SQLAlchemy engine and session factory for
interacting with a SQLite database stored in the `data/` folder.

For production deployments you may want to replace this with a
PostgreSQL connection managed by Supabase or another cloud provider.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./data/app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
