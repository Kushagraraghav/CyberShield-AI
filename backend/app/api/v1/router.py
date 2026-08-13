"""API v1 router - aggregates all v1 endpoints."""

from fastapi import APIRouter

from app.api.v1.endpoints import health

router = APIRouter(prefix="/api/v1")

# Include health endpoints
router.include_router(health.router)
