from app.services import user_services


def setup_function():
    user_services.users.clear()
    user_services.current_id = 1


# --- Teste antigo adaptado ---
def test_should_not_allow_duplicate_users():
    user_services.create_user({"name": "Leonardo", "email": "leo1@test.com"})
    user = user_services.create_user({"name": "Leonardo", "email": "leo2@test.com"})
    assert user is None


# --- 10 Novos Testes Unitários ---
def test_create_user_with_email_success():
    user = user_services.create_user({"name": "Alice", "email": "alice@test.com"})
    assert user is not None
    assert user.get("email") == "alice@test.com"


def test_create_user_without_email_fails():
    user = user_services.create_user({"name": "Bob"})
    assert user is None


def test_create_user_invalid_email_fails():
    user = user_services.create_user({"name": "Charlie", "email": "charlie_no_at.com"})
    assert user is None


def test_create_user_duplicate_email_fails():
    user_services.create_user({"name": "David", "email": "david@test.com"})
    user = user_services.create_user({"name": "David2", "email": "david@test.com"})
    assert user is None


def test_get_all_users_empty():
    users = user_services.get_all_users()
    assert len(users) == 0


def test_get_all_users_with_data():
    user_services.create_user({"name": "Eve", "email": "eve@test.com"})
    users = user_services.get_all_users()
    assert len(users) == 1


def test_update_user_name_and_email_success():
    user = user_services.create_user({"name": "Frank", "email": "frank@test.com"})
    updated = user_services.update_user(
        user["id"], {"name": "Frank Updated", "email": "frank2@test.com"}
    )
    assert updated is not None
    assert updated["name"] == "Frank Updated"
    assert updated.get("email") == "frank2@test.com"


def test_update_user_with_duplicate_email_fails():
    user_services.create_user({"name": "Grace", "email": "grace@test.com"})
    user2 = user_services.create_user({"name": "Heidi", "email": "heidi@test.com"})
    updated = user_services.update_user(
        user2["id"], {"name": "Heidi", "email": "grace@test.com"}
    )
    assert updated is None


def test_delete_user_success():
    user = user_services.create_user({"name": "Ivan", "email": "ivan@test.com"})
    user_services.delete_user(user["id"])
    assert len(user_services.get_all_users()) == 0


def test_delete_user_not_found():
    user_services.create_user({"name": "Judy", "email": "judy@test.com"})
    user_services.delete_user(999)
    assert len(user_services.get_all_users()) == 1
