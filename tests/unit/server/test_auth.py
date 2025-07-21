import pytest
from fastapi.testclient import TestClient
from src.server.app import app, ADMIN_TOKEN

@pytest.fixture
def client():
    return TestClient(app)


def test_record_user_and_admin_listing(client):
    resp = client.post("/api/users/record", json={"email": "user@example.com"})
    assert resp.status_code == 200
    resp = client.post("/api/admin/login", json={"username": "admin@gmail.com", "password": "admin"})
    assert resp.status_code == 200
    token = resp.json()["token"]
    assert token == ADMIN_TOKEN
    resp = client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert "user@example.com" in resp.json()


def test_admin_login_fail(client):
    resp = client.post("/api/admin/login", json={"username": "x", "password": "y"})
    assert resp.status_code == 401
