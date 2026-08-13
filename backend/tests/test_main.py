"""Tests for FastAPI application."""

from fastapi.testclient import TestClient

from app.main import app


def test_app_creation():
    """Test that FastAPI application is created."""
    assert app is not None
    assert app.title == "CyberShield AI"


def test_root_endpoint():
    """Test the root endpoint."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "api_docs" in data


def test_docs_endpoint():
    """Test that API documentation endpoints are available."""
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200
