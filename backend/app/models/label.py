from datetime import UTC, datetime

from app.extensions import db


class Label(db.Model):
    __tablename__ = "labels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default="#94a3b8")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="user_labels", lazy=True)
    tasks = db.relationship(
        "Task",
        secondary="task_labels",
        back_populates="labels_on_tasks",
    )
