from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app.models.user import User


def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user or not user.role or user.role.name not in roles:
                return jsonify({"error": "You do not have permission to perform this action"}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator
