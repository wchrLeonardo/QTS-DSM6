users = []
current_id = 1


def get_all_users():
    return users


def get_user_by_id(user_id):
    return next((u for u in users if u["id"] == user_id), None)


def is_valid_email(email):
    return "@" in email


def create_user(data):
    global current_id

    if "name" not in data or "email" not in data:
        return None

    email = data["email"]
    if not is_valid_email(email):
        return None

    existing_user = next(
        (u for u in users if u["name"] == data["name"] or u.get("email") == email), None
    )

    if existing_user:
        return None

    user = {"id": current_id, "name": data["name"], "email": email}
    users.append(user)
    current_id += 1
    return user


def update_user(user_id, data):
    user = get_user_by_id(user_id)
    if not user:
        return None

    if "email" in data:
        email = data["email"]
        if not is_valid_email(email):
            return None
        existing_user = next(
            (u for u in users if u.get("email") == email and u["id"] != user_id), None
        )
        if existing_user:
            return None
        user["email"] = email

    if "name" in data:
        user["name"] = data["name"]

    return user


def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
