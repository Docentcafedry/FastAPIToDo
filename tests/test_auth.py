from .conftest import client


def test_signup(session):
    user_create_response = client.post(
        "/auth/signup",
        json={
            "email": "user1@example.com",
            "username": "string1",
            "first_name": "string",
            "last_name": "string",
            "password": "string",
            "role": "string",
            "is_active": True,
            "number": "string",
        },
    )
    assert user_create_response.status_code == 201


def test_signup_error_validation(session):
    user_create_response = client.post(
        "/auth/signup",
        json={
            "email": "user1@example",
            "username": "string1",
            "first_name": "string",
            "last_name": "string",
            "password": "string",
            "role": "string",
            "is_active": True,
            "number": "string",
        },
    )
    assert user_create_response.status_code == 422


def test_get_token(session, create_user):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201


def test_get_token_bad_credentials(session, create_user):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string12", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 401


def test_get_current_user(session, create_user):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )

    response = client.get(
        f"/auth/users/me?token={user_obtain_jwt.json()['access_token']}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "string1",
        "role": "admin",
        "is_active": True,
    }


def test_get_current_user_without_token(session, create_user):
    response = client.get("/auth/users/me")
    assert response.status_code == 422


def test_change_user_password(session, create_user):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )

    response = client.patch(
        f"/auth/users/change_password?token={user_obtain_jwt.json()['access_token']}",
        json={"new_password": "string", "confirm_new_password": "string"},
    )
    assert response.status_code == 204
