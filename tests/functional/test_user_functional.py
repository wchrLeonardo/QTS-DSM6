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
    response = client.post("/users", json={"name": "Full Flow"})
    assert response.status_code == 201
    user_id = response.get_json()["id"]

    # Get
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    # Update
    response = client.put(f"/users/{user_id}", json={"name": "Full Flow Updated"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Full Flow Updated"

    # Delete
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify not found
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_list_users(client):
    client.post("/users", json={"name": "User 1"})
    client.post("/users", json={"name": "User 2"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_create_and_list_three_users(client):
    # cria 3 usuários
    client.post("/users", json={"name": "User 1"})
    client.post("/users", json={"name": "User 2"})
    client.post("/users", json={"name": "User 3"})

    # lista os usuários
    response = client.get("/users")

    # valida a quantidade de usuários
    assert response.status_code == 200
    assert len(response.get_json()) == 3

def test_should_return_400_when_user_already_exists(client):
    client.post("/users", json={"name": "Leonardo"})

    response = client.post("/users", json={"name": "Leonardo"})

    assert response.status_code == 400