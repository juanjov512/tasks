from authz.decorators import role_required
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.user import UserService

user_bp = Blueprint("user", __name__)


@user_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@jwt_required()
@role_required(["admin"])
def update_user_role(user_id):
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        result = UserService.update_user_role(user_id, admin_id, data["role_name"])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
