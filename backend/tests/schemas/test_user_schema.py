from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.auth import UserCreate, UserLogin, UserResponse, UserUpdate


def test_user_create_schema():
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Password123!",
    }

    user = UserCreate(**data)

    assert user.email == data["email"]
    assert user.username == data["username"]
    assert user.password == data["password"]


def test_user_create_schema_validation():
    data = {"email": "notanemail", "username": "testuser", "password": "Password123!"}

    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_login_schema():
    data = {"email": "test@example.com", "password": "Password123!"}

    login = UserLogin(**data)

    assert login.email == data["email"]
    assert login.password == data["password"]


def test_user_update_schema():
    data = {
        "username": "newusername",
        "email": "new@example.com",
        "password": "NewPassword123!",
    }

    update = UserUpdate(**data)

    assert update.username == data["username"]
    assert update.email == data["email"]
    assert update.password == data["password"]


def test_user_response_schema():
    data = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "role_id": 1,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }

    response = UserResponse(**data)

    assert response.id == data["id"]
    assert response.email == data["email"]
    assert response.username == data["username"]
    assert response.role_id == data["role_id"]
    assert isinstance(response.created_at, datetime)
    assert isinstance(response.updated_at, datetime)
