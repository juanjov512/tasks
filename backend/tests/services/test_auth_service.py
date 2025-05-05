import pytest

from app.models import User
from app.services.auth import AuthService


def test_register_user(init_database):
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "Password123!",
    }

    user = AuthService.register_user(user_data)

    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.id is not None

    db_user = User.query.get(user.id)
    assert db_user is not None
    assert db_user.email == user_data["email"]


def test_register_duplicate_email(init_database):
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "Password123!",
    }
    AuthService.register_user(user_data)

    duplicate_data = {
        "email": "duplicate@example.com",
        "username": "user2",
        "password": "Password123!",
    }

    with pytest.raises(ValueError) as exc_info:
        AuthService.register_user(duplicate_data)
    assert "Email already registered" in str(exc_info.value)


def test_login_user(init_database):
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "Password123!",
    }
    AuthService.register_user(user_data)

    login_data = {"email": "login@example.com", "password": "Password123!"}
    tokens = AuthService.login_user(login_data)
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None


def test_login_invalid_credentials(init_database):
    user_data = {
        "email": "invalid@example.com",
        "username": "invaliduser",
        "password": "Password123!",
    }
    AuthService.register_user(user_data)

    login_data = {"email": "invalid@example.com", "password": "WrongPassword123!"}
    with pytest.raises(ValueError) as exc_info:
        AuthService.login_user(login_data)
    assert "Invalid credentials" in str(exc_info.value)
