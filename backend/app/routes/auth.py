from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)

from ..services.auth import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        user = AuthService.register_user(data)
        return jsonify(user.model_dump()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        tokens = AuthService.login_user(data)

        response = jsonify(tokens.model_dump())
        set_access_cookies(response, tokens.access_token)
        set_refresh_cookies(response, tokens.refresh_token)

        return response, 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = AuthService.get_user_profile(user_id)
        return jsonify(user.model_dump()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        user = AuthService.update_user_profile(user_id, data)
        return jsonify(user.model_dump()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
