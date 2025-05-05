from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.task import TaskService

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    try:
        user_id = get_jwt_identity()
        tasks = TaskService.get_user_tasks(user_id)
        return jsonify([task.model_dump() for task in tasks]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        task = TaskService.create_task(user_id, data)
        return jsonify(task.model_dump()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    try:
        user_id = get_jwt_identity()
        task = TaskService.get_task(task_id, user_id)
        return jsonify(task.model_dump()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        task = TaskService.update_task(task_id, user_id, data)
        return jsonify(task.model_dump()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    try:
        user_id = get_jwt_identity()
        TaskService.delete_task(task_id, user_id)
        return "", 204
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@tasks_bp.route("/<int:task_id>/labels", methods=["POST"])
@jwt_required()
def add_labels_to_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        result = TaskService.add_labels_to_task(task_id, user_id, data.get("label_ids", []))
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@tasks_bp.route("/<int:task_id>/labels/<int:label_id>", methods=["DELETE"])
@jwt_required()
def remove_label_from_task(task_id, label_id):
    user_id = get_jwt_identity()
    try:
        result = TaskService.remove_label_from_task(task_id, user_id, label_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 404
