from datetime import UTC, datetime

from app.extensions import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    users = db.relationship("User", backref="role", lazy=True)
