from .conftest import client


def test_update_number(session, create_user):
    user_obtain_jwt = client.post(
        "/auth/token", data={"username": "string1", "password": "123456"}
    )
    assert user_obtain_jwt.status_code == 201
    response = client.patch(f"/users/change-number?token={user_obtain_jwt.json()['access_token']}", json={"number": "432432432432"})
    assert response.status_code == 204
