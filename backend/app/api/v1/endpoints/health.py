"""Health check endpoint."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from app.core.logging import get_logger
from app.db.session import get_db_connection

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Verifies:
    - Application is running
    - Database connectivity
    
    Returns:
        dict: Health status response.
        
    Raises:
        HTTPException: If health check fails.
    """
    try:
        # Check database connectivity
        db = get_db_connection()
        try:
            db.execute(text("SELECT 1"))
            db.close()
            db_status = "healthy"
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {str(e)}")
            db_status = "unhealthy"

        return {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "database": db_status,
            "message": "CyberShield AI backend is running",
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Health check failed",
        )
