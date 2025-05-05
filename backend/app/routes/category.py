from authz.decorators import role_required
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.category import CategoryService

category_bp = Blueprint("category", __name__)


@category_bp.route("/categories", methods=["GET"])
@jwt_required()
def get_categories():
    try:
        categories = CategoryService.get_all_categories()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@category_bp.route("/categories/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    try:
        category = CategoryService.get_category_by_id(category_id)
        return jsonify(category), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@category_bp.route("/categories", methods=["POST"])
@jwt_required()
@role_required(["admin"])
def create_category():
    data = request.get_json()
    try:
        result = CategoryService.create_category(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@category_bp.route("/categories/<int:category_id>", methods=["PUT"])
@jwt_required()
@role_required(["admin"])
def update_category(category_id):
    data = request.get_json()
    try:
        result = CategoryService.update_category(category_id, data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@category_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required()
@role_required(["admin"])
def delete_category(category_id):
    try:
        result = CategoryService.delete_category(category_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
