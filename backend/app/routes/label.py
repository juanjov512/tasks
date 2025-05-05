from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.label import LabelService

label_bp = Blueprint("label", __name__)


@label_bp.route("/labels", methods=["GET"])
@jwt_required()
def get_labels():
    try:
        user_id = get_jwt_identity()
        labels = LabelService.get_user_labels(user_id)
        return jsonify(labels), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@label_bp.route("/labels/<int:label_id>", methods=["GET"])
@jwt_required()
def get_label(label_id):
    try:
        user_id = get_jwt_identity()
        label = LabelService.get_label_by_id(label_id, user_id)
        return jsonify(label), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@label_bp.route("/labels", methods=["POST"])
@jwt_required()
def create_label():
    data = request.get_json()
    try:
        user_id = get_jwt_identity()
        result = LabelService.create_label(user_id, data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@label_bp.route("/labels/<int:label_id>", methods=["PUT"])
@jwt_required()
def update_label(label_id):
    data = request.get_json()
    try:
        user_id = get_jwt_identity()
        result = LabelService.update_label(label_id, user_id, data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@label_bp.route("/labels/<int:label_id>", methods=["DELETE"])
@jwt_required()
def delete_label(label_id):
    try:
        user_id = get_jwt_identity()
        result = LabelService.delete_label(label_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
