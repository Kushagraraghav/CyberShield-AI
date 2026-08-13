"""Centralized exception handling."""

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging import get_logger

logger = get_logger(__name__)


class CyberShieldException(Exception):
    """Base exception for CyberShield AI application."""

    pass


class DatabaseException(CyberShieldException):
    """Database-related exception."""

    def __init__(self, message: str = "Database operation failed"):
        self.message = message
        super().__init__(self.message)


class ValidationException(CyberShieldException):
    """Validation-related exception."""

    def __init__(self, message: str = "Validation failed"):
        self.message = message
        super().__init__(self.message)


def handle_db_exception(exc: SQLAlchemyError) -> HTTPException:
    """
    Convert database exceptions to HTTP exceptions.
    
    Args:
        exc: SQLAlchemy exception.
        
    Returns:
        HTTPException: HTTP error response.
    """
    logger.error(f"Database error: {str(exc)}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="A database error occurred. Please try again later.",
    )


def handle_validation_exception(exc: ValidationException) -> HTTPException:
    """
    Convert validation exceptions to HTTP exceptions.
    
    Args:
        exc: Validation exception.
        
    Returns:
        HTTPException: HTTP error response.
    """
    logger.warning(f"Validation error: {exc.message}")
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=exc.message,
    )
