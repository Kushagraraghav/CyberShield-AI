"""Tests for health check endpoint."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    """Test the health endpoint responds."""
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "message" in data


def test_health_status_values():
    """Test that health status has expected values."""
    client = TestClient(app)
    response = client.get("/api/v1/health")
    data = response.json()
    # Status should be 'healthy' or 'degraded'
    assert data["status"] in ["healthy", "degraded"]
    # Database should be 'healthy' or 'unhealthy'
    assert data["database"] in ["healthy", "unhealthy"]
