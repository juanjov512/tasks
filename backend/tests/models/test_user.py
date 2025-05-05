from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import User


def test_user_creation(init_database):
    user = User(email="newuser@example.com", username="newuser", role_id=1)
    user.set_password("password123")
    init_database.session.add(user)
    init_database.session.commit()

    assert user.check_password("password123")
    assert not user.check_password("wrongpassword")

    assert user.email == "newuser@example.com"
    assert user.username == "newuser"
    assert user.role_id == 1
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_relationships():
    user = User(email="testuser2@example.com", username="testuser2", role_id=1)
    user.set_password("password123")

    assert hasattr(user, "tasks")
    assert hasattr(user, "labels")
    assert hasattr(user, "role")


def test_user_unique_constraints(init_database):
    user1 = User(email="unique@example.com", username="uniqueuser", role_id=1)
    user1.set_password("password123")
    init_database.session.add(user1)
    init_database.session.commit()

    user2 = User(email="unique@example.com", username="anotheruser", role_id=1)
    user2.set_password("password123")
    init_database.session.add(user2)

    with pytest.raises(IntegrityError):
        init_database.session.commit()

    init_database.session.rollback()

    user3 = User(email="another@example.com", username="uniqueuser", role_id=1)
    user3.set_password("password123")
    init_database.session.add(user3)

    with pytest.raises(IntegrityError):
        init_database.session.commit()
