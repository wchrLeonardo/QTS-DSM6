import pytest
from app import create_app
from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1
    return app.test_client()


def test_api_create_user_with_email(client):
    response = client.post("/users", json={"name": "Alice", "email": "alice@test.com"})
    assert response.status_code == 201
    assert response.get_json()["email"] == "alice@test.com"


def test_api_create_user_missing_email_returns_400(client):
    response = client.post("/users", json={"name": "Bob"})
    assert response.status_code == 400


def test_api_create_user_duplicate_email_returns_400(client):
    client.post("/users", json={"name": "Charlie", "email": "charlie@test.com"})
    response = client.post(
        "/users", json={"name": "Charlie2", "email": "charlie@test.com"}
    )
    assert response.status_code == 400


def test_api_update_user_email(client):
    response = client.post("/users", json={"name": "David", "email": "david@test.com"})
    user_id = response.get_json()["id"]
    update_resp = client.put(
        f"/users/{user_id}", json={"name": "David", "email": "david_new@test.com"}
    )
    assert update_resp.status_code == 200
    assert update_resp.get_json()["email"] == "david_new@test.com"


def test_api_update_user_invalid_email_returns_400(client):
    response = client.post("/users", json={"name": "Eve", "email": "eve@test.com"})
    user_id = response.get_json()["id"]
    update_resp = client.put(
        f"/users/{user_id}", json={"name": "Eve", "email": "invalid"}
    )
    assert update_resp.status_code == 400
