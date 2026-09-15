from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_email():
    return f"test-{uuid4()}@example.com"


def test_register_user():
    email = create_test_email()

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["email"] == email


def test_login_user():
    email = create_test_email()

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "strongpassword123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "strongpassword123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_protected_me_endpoint():
    email = create_test_email()

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "strongpassword123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "strongpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert me_response.status_code == 200
    assert me_response.json()["email"] == email