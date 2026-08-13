"""Database session and engine configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


# Create SQLAlchemy engine with psycopg driver
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=NullPool,  # Use NullPool for better compatibility with async contexts
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    Dependency for getting database session.
    
    Yields:
        Session: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_connection() -> Session:
    """
    Get a direct database session (for non-async contexts).
    
    Returns:
        Session: Database session.
    """
    return SessionLocal()
