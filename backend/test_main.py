import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the /health endpoint returns 200 and 'ok' status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_contact_form_success():
    """Test successful contact form submission."""
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "received"}

def test_contact_form_invalid_email():
    """Test contact form with invalid email should fail pydantic validation."""
    payload = {
        "name": "John Doe",
        "email": "invalid-email",
        "message": "Hello"
    }
    # FastAPI returns 422 Unprocessable Entity for Pydantic validation errors
    response = client.post("/contact", json=payload)
    assert response.status_code == 422

def test_contact_form_missing_fields():
    """Test contact form with missing required fields."""
    payload = {
        "name": "John Doe"
        # email and message missing
    }
    response = client.post("/contact", json=payload)
    assert response.status_code == 422
