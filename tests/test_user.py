from jose import jwt
import pytest

from app import schemas
from app.config import settings


def test_root(client, session):
    response = client.get("/")
    assert response.json().get("message") == "Hello World!"
    assert response.status_code == 200


def test_create_user(client, session):
    response = client.post("/sqlalchemy/users", json={"email": "test@test.com", "password": "test"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "test@test.com"
    assert response.status_code == 201


def test_get_user(client, session, test_user):
    response = client.get("/sqlalchemy/users/1")
    new_user = schemas.UserOut(**response.json())
    assert new_user.id == 1
    assert response.status_code == 200


def test_get_users(client, session, test_user):
    response = client.get("/sqlalchemy/users")
    assert response.status_code == 200


def test_update_user(client, session, test_user):
    response = client.put("/sqlalchemy/users/1", json={"email": "updated_test@test.com", "password": "updated_test"})
    updated_user = schemas.UserOut(**response.json())
    assert updated_user.email == "updated_test@test.com"
    assert response.status_code == 200


def test_delete_user(client, session, test_user):
    response = client.delete("/sqlalchemy/users/1")
    assert response.status_code == 204


def test_login_user(client, session, test_user):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code", [
        ("wrongemail@test.com", "test", 403),
        ("test@test.com", "wrongpassword", 403),
        ("wrongemail@test.com", "wrongpassword", 403),
        (None, "test", 422),
        ("test@test.com", None, 422)
    ]
)
def test_incorrect_login(client, session, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid Credentials"

