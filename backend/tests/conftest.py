# flake8: noqa: E402
import os
import sys
from pathlib import Path

HTTP_OK = 200

# Env vars config for tests
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import Role, User


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()

        admin_role = Role(name="admin")
        user_role = Role(name="user")
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()

        test_user = User(email="test@example.com", username="testuser", role_id=user_role.id)
        test_user.set_password("password123")
        db.session.add(test_user)
        db.session.commit()

        yield db

        db.session.rollback()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def auth_headers(client):
    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "password123"})

    assert response.status_code == HTTP_OK, (
        f"Login failed with status {response.status_code}. Response: {response.data}"
    )

    response_data = response.get_json()
    assert response_data is not None, "Response is None"
    assert "access_token" in response_data, f"Response does not contain access_token: {response_data}"

    token = response_data["access_token"]
    return {"Authorization": f"Bearer {token}"}
