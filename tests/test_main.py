import pytest
from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    """
    Tests if the root path '/' successfully returns the HTML frontend.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "Analisador de Contratos com IA" in response.text

def test_login_success(client: TestClient):
    """
    Tests successful login with correct credentials.
    """
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

def test_login_failure_wrong_password(client: TestClient):
    """
    Tests failed login with incorrect credentials.
    """
    response = client.post(
        "/login",
        data={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Usuário ou senha inválidos"}

def test_login_failure_wrong_username(client: TestClient):
    """
    Tests failed login with incorrect credentials.
    """
    response = client.post(
        "/login",
        data={"username": "notadmin", "password": "admin"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Usuário ou senha inválidos"}