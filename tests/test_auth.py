import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_login_success():
    response = client.post("/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/login", data={"username": "admin", "password": "wrong"})
    assert response.status_code == 400