from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def random_email():
    return f"user_{uuid.uuid4().hex[:8]}@example.com"

def random_username():
    return f"user_{uuid.uuid4().hex[:8]}"

def test_create_user():
    user_data = {
        "username": random_username(),
        "email": random_email(),
        "full_name": "Nicholas",
        "role": "admin"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]

def test_read_user():
    user_data = {
        "username": random_username(),
        "email": random_email(),
        "full_name": "Nicholas",
        "role": "admin"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == user_data["username"]

def test_update_user():
    user_data = {
        "username": random_username(),
        "email": random_email(),
        "full_name": "Nicholas",
        "role": "admin"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    updated_data = {
        "username": random_username(),
        "email": random_email(),
        "full_name": "Nicholas",
        "role": "admin"
    }
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == updated_data["username"]
    assert data["email"] == updated_data["email"]
    assert data["full_name"] == updated_data["full_name"]
    assert data["role"] == updated_data["role"]

def test_delete_user():
    user_data = {
        "username": random_username(),
        "email": random_email(),
        "full_name": "Nicholas",
        "role": "admin"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
