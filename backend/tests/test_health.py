import pytest
import sys
import os

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_health_endpoint_status_code(client):
    """Test that GET /api/health returns HTTP 200."""
    response = client.get("/api/health")
    assert response.status_code == 200


def test_health_endpoint_json_payload(client):
    """Test that GET /api/health returns expected JSON response."""
    response = client.get("/api/health")
    data = response.get_json()
    assert data is not None
    assert data.get("status") == "success"
    assert data.get("message") == "DocuEase backend is running"


def test_health_endpoint_content_type(client):
    """Test that GET /api/health returns application/json header."""
    response = client.get("/api/health")
    assert "application/json" in response.content_type


def test_root_endpoint(client):
    """Test that GET / returns API metadata and 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("name") == "DocuEase API"
