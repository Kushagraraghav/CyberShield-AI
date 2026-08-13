"""FastAPI application factory and setup."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1.router import router as api_v1_router
from app.db.session import engine
from app.db.base import Base

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    logger.info(f"Starting {settings.app_name} in {settings.app_env} mode")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    # Setup logging
    setup_logging()

    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description="AI-Assisted SOC and Digital Forensics Platform",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API v1 routes
    app.include_router(api_v1_router)

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": "0.1.0",
            "api_docs": "/docs",
        }

    logger.info(f"FastAPI application configured: {settings.app_name}")
    return app


# Create application instance
app = create_app()
