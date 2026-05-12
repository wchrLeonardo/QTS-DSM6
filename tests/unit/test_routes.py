import pytest
from app import create_app


from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1
    return app.test_client()


def test_create_user_success(client):
    response = client.post("/users", json={"name": "Usuário 1", "email": "u1@test.com"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Usuário 1"


def test_create_user_missing_name(client):
    response = client.post("/users", json={"email": "u1@test.com"})
    assert response.status_code == 400
    assert "Dados inválidos" in response.get_json()["message"]
    response = client.get("/users")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_user(client):
    client.post("/users", json={"name": "Teste", "email": "teste@test.com"})
    response = client.get("/users/1")
    assert response.status_code == 200


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.get_json()["message"]


def test_delete_user(client):
    client.post("/users", json={"name": "Delete", "email": "del@test.com"})
    response = client.delete("/users/1")
    assert response.status_code == 204


def test_update_user_success(client):
    # 1. Criar usuário
    response = client.post("/users", json={"name": "Update", "email": "up@test.com"})
    assert response.status_code == 201

    user_id = response.get_json()["id"]

    # 2. Atualizar usuário
    response = client.put(
        f"/users/{user_id}", json={"name": "Update 2", "email": "up2@test.com"}
    )
    assert response.status_code == 200
    assert response.get_json()["name"] == "Update 2"
