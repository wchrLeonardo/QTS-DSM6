import pytest
from app import create_app
from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1
    return app.test_client()


def test_user_full_flow(client):
    # Create
    response = client.post(
        "/users", json={"name": "Full Flow", "email": "full@test.com"}
    )
    assert response.status_code == 201
    user_id = response.get_json()["id"]

    # Get
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    # Update
    response = client.put(
        f"/users/{user_id}",
        json={"name": "Full Flow Updated", "email": "full_up@test.com"},
    )
    assert response.status_code == 200
    assert response.get_json()["name"] == "Full Flow Updated"
    assert response.get_json()["email"] == "full_up@test.com"

    # Delete
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify not found
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_list_users(client):
    client.post("/users", json={"name": "User 1", "email": "u1@test.com"})
    client.post("/users", json={"name": "User 2", "email": "u2@test.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_create_and_list_three_users(client):
    client.post("/users", json={"name": "User 1", "email": "a@test.com"})
    client.post("/users", json={"name": "User 2", "email": "b@test.com"})
    client.post("/users", json={"name": "User 3", "email": "c@test.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_should_return_400_when_user_already_exists(client):
    client.post("/users", json={"name": "Leonardo", "email": "leo@test.com"})
    response = client.post(
        "/users", json={"name": "Leonardo2", "email": "leo@test.com"}
    )
    assert response.status_code == 400


# --- 3 Novos Testes Funcionais ---
def test_functional_register_same_email_fails(client):
    resp1 = client.post("/users", json={"name": "Func 1", "email": "func@test.com"})
    assert resp1.status_code == 201
    resp2 = client.post("/users", json={"name": "Func 2", "email": "func@test.com"})
    assert resp2.status_code == 400


def test_functional_update_name_and_email(client):
    resp1 = client.post("/users", json={"name": "Old Name", "email": "old@test.com"})
    user_id = resp1.get_json()["id"]

    resp2 = client.put(
        f"/users/{user_id}", json={"name": "New Name", "email": "new@test.com"}
    )
    assert resp2.status_code == 200

    resp3 = client.get(f"/users/{user_id}")
    assert resp3.get_json()["name"] == "New Name"
    assert resp3.get_json()["email"] == "new@test.com"


def test_functional_delete_all_users_sequentially(client):
    client.post("/users", json={"name": "U1", "email": "u1@test.com"})
    client.post("/users", json={"name": "U2", "email": "u2@test.com"})

    users = client.get("/users").get_json()
    assert len(users) == 2

    for u in users:
        client.delete(f"/users/{u['id']}")

    users_after = client.get("/users").get_json()
    assert len(users_after) == 0
