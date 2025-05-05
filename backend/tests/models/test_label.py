from datetime import datetime

from app.models import Label, User


def test_label_creation(init_database):
    user = User(email="labeluser@example.com", username="labeluser", role_id=1)
    user.set_password("password123")
    init_database.session.add(user)
    init_database.session.commit()

    label = Label(name="Test Label", color="#FF0000", user_id=user.id)
    init_database.session.add(label)
    init_database.session.commit()

    assert label.name == "Test Label"
    assert label.color == "#FF0000"
    assert label.user_id == user.id
    assert isinstance(label.created_at, datetime)


def test_label_relationships(init_database):
    user = User(email="labeluser2@example.com", username="labeluser2", role_id=1)
    user.set_password("password123")
    init_database.session.add(user)
    init_database.session.commit()

    label = Label(name="Test Label 2", user_id=user.id)
    init_database.session.add(label)
    init_database.session.commit()

    assert hasattr(label, "user")
    assert hasattr(label, "tasks")
    assert label.user.id == user.id


def test_label_default_color(init_database):
    user = User(email="labeluser3@example.com", username="labeluser3", role_id=1)
    user.set_password("password123")
    init_database.session.add(user)
    init_database.session.commit()

    label = Label(name="Test Label 3", user_id=user.id)
    init_database.session.add(label)
    init_database.session.commit()

    assert label.color == "#94a3b8"
