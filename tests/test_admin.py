from .conftest import client


def test_get_todos(session):
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
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "string"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.get(f"/todos/?token={user_obtain_jwt.json()['access_token']}")
    assert response.status_code == 200
    assert response.json() == []


def test_get_todos_not_empty(session, create_todo):
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
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "string"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.get(f"/todos/?token={user_obtain_jwt.json()['access_token']}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_todos_not_admin_user(session, create_user, create_todo):
    user_create_response_second = client.post(
        "/auth/signup",
        json={
            "email": "user2@example.com",
            "username": "string2",
            "first_name": "string",
            "last_name": "string",
            "password": "string",
            "role": "string",
            "is_active": True,
            "number": "string",
        },
    )
    assert user_create_response_second.status_code == 201
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string2", "password": "string"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.get(f"/todos/?token={user_obtain_jwt.json()['access_token']}")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_todo_admin_user(session, create_user, create_todo):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.get(
        f"/admin/todos/1?token={user_obtain_jwt.json()['access_token']}"
    )
    assert response.status_code == 200


def test_update_todo_admin_user(session, create_user, create_todo):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.put(
        f"/admin/todos/update/1?token={user_obtain_jwt.json()['access_token']}",
        json={
            "name": "string",
            "description": "string",
            "priority": 1,
            "is_done": False,
        },
    )
    assert response.status_code == 204


def test_update_todo_different_user(session, create_user, create_todo):
    user_create_response_second = client.post(
        "/auth/signup",
        json={
            "email": "user2@example.com",
            "username": "string2",
            "first_name": "string",
            "last_name": "string",
            "password": "string",
            "role": "string",
            "is_active": True,
            "number": "string",
        },
    )
    assert user_create_response_second.status_code == 201
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string2", "password": "string"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.put(
        f"/admin/todos/update/1?token={user_obtain_jwt.json()['access_token']}",
        json={
            "name": "string",
            "description": "string",
            "priority": 1,
            "is_done": False,
        },
    )
    assert response.status_code == 403


def test_delete_todo_admin_user(session, create_user, create_todo):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.delete(
        f"/admin/todos/delete/1?token={user_obtain_jwt.json()['access_token']}",
    )
    assert response.status_code == 204


def test_delete_todo_different_user(session, create_user, create_todo):
    user_create_response_second = client.post(
        "/auth/signup",
        json={
            "email": "user2@example.com",
            "username": "string2",
            "first_name": "string",
            "last_name": "string",
            "password": "string",
            "role": "string",
            "is_active": True,
            "number": "string",
        },
    )
    assert user_create_response_second.status_code == 201
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string2", "password": "string"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.delete(
        f"/admin/todos/delete/1?token={user_obtain_jwt.json()['access_token']}",
    )
    assert response.status_code == 403
