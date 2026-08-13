"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add backend to path
backend_path = str(Path(__file__).parent.parent)
sys.path.insert(0, backend_path)

# Set test environment
os.environ["APP_ENV"] = "testing"
os.environ["DEBUG"] = "true"


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for FastAPI app."""
    from app.main import app

    return TestClient(app)
