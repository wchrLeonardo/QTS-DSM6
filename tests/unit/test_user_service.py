from app.services import user_service

def test_should_not_allow_duplicate_users():
    user_service.users.clear()
    user_service.current_id = 1

    user_service.create_user({"name": "Leonardo"})

    user = user_service.create_user({"name": "Leonardo"})

    assert user is None

