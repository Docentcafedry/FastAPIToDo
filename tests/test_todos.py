import random

from .conftest import client, get_random_string
import pytest
from sqlalchemy import select
from models import User

random_integer = random.randint(0, 100)


@pytest.mark.asyncio
async def test_get_todos(session):
    user_create_response = client.post(
        "/auth/signup",
        json={
            "email": f"user{random_integer}@example.com",
            "username": f"string{random_integer}",
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
        "/auth/token",
        data={"username": f"string{random_integer}", "password": "string"},
    )
    print(user_obtain_jwt.json()["access_token"])
    assert user_obtain_jwt.status_code == 201
    response = client.get(f"/todos/?token={user_obtain_jwt.json()['access_token']}")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_todo(session, create_user, create_todo):
    user_obtain_jwt = client.post(
        "/auth/token",
        data={"username": "string1", "password": "123456"},
    )
    assert user_obtain_jwt.status_code == 201
    response = client.get(f"/todos/1?token={user_obtain_jwt.json()['access_token']}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_todo_404(session, create_user):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.get(f"/todos/1?token={user_obtain_jwt.json()['access_token']}")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_todo(session, create_user):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.post(
        f"/todos/create?token={user_obtain_jwt.json()['access_token']}",
        json={
            "name": "string",
            "description": "string",
            "priority": 1,
            "is_done": False,
        },
    )
    res = await session.execute(select(User).where(User.username == "string1"))
    user = res.scalar_one_or_none()
    assert user.username == "string1"
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_todo_without_token(session):
    response = client.post(
        "/todos/create",
        data={
            "name": "string",
            "description": "stringd",
            "priority": 1,
            "is_done": False,
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_todo(session, create_user, create_todo):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.put(
        f"/todos/update/1?token={user_obtain_jwt.json()['access_token']}",
        json={
            "name": "string",
            "description": "string",
            "priority": 1,
            "is_done": False,
        },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_todo_without_token(session, create_user, create_todo):
    response = client.put(
        f"/todos/update/1",
        data={
            "name": "string",
            "description": "string",
            "priority": 1,
            "is_done": False,
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_todo(session, create_user, create_todo):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.delete(
        f"/todos/delete/1?token={user_obtain_jwt.json()['access_token']}",
    )
    assert response.status_code == 204
