from .conftest import client, get_random_string


def test_get_todos(session):
    user_create_response = client.post(
        "/auth/signup",
        json=
            {
                "email": "user1@example.com",
                "username": "string1",
                "first_name": "string",
                "last_name": "string",
                "password": "string",
                "role": "string",
                "is_active": True,
                "number": "string",
            }

    )
    assert user_create_response.status_code == 201
    user_obtain_jwt = client.post("/auth/token", data={"username": "string1", "password": "string"})
    assert user_obtain_jwt.status_code == 201
    response = client.get(f"/todos/?token={user_obtain_jwt.json()['access_token']}")
    print(response)
    assert response.status_code == 200
    assert response.json() == []


