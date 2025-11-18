import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User created successfully"
    assert "data" in data
    assert data["data"]["username"] == "testuser"

def test_get_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data

def test_get_user_by_id():
    response = client.get("/api/v1/users/1")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert data["success"] is True
        assert "data" in data