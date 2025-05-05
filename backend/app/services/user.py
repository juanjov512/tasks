from typing import Any

from app import db
from app.models import Role, User


class UserService:
    @staticmethod
    def update_user_role(user_id: int, admin_id: int, role_name: str) -> dict[str, Any]:
        try:
            admin = User.query.get(admin_id)
            if not admin or not admin.role or admin.role.name != "admin":
                raise ValueError("You do not have permission to change roles")

            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")

            role = Role.query.filter_by(name=role_name).first()
            if not role:
                raise ValueError("Invalid role")

            user.role_id = role.id
            db.session.commit()

            return {"message": f"Role updated to {role_name} successfully"}
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e
