from unittest.mock import MagicMock, patch

from flask import jsonify

from app.authz.decorators import role_required

HTTP_OK = 200
HTTP_FORBIDDEN = 403


def test_role_required(app):
    with app.app_context():
        mock_function = MagicMock(return_value=(jsonify({"message": "success"}), HTTP_OK))

        mock_user = MagicMock()
        mock_role = MagicMock()
        mock_role.name = "admin"
        mock_user.role = mock_role

        with (
            patch("app.authz.decorators.get_jwt_identity", return_value=1),
            patch("app.authz.decorators.User.query") as mock_query,
        ):
            mock_query.get.return_value = mock_user

            decorated_function = role_required(["admin"])(mock_function)

            response = decorated_function()
            assert response[1] == HTTP_OK
            assert response[0].get_json()["message"] == "success"

            mock_role.name = "user"
            response = decorated_function()
            assert response[1] == HTTP_FORBIDDEN
            assert response[0].get_json()["error"] == "You do not have permission to perform this action"


def test_role_required_no_user(app):
    with app.app_context():
        mock_function = MagicMock(return_value=(jsonify({"message": "success"}), HTTP_OK))

        with (
            patch("app.authz.decorators.get_jwt_identity", return_value=1),
            patch("app.authz.decorators.User.query") as mock_query,
        ):
            mock_query.get.return_value = None

            decorated_function = role_required(["admin"])(mock_function)

            response = decorated_function()
            assert response[1] == HTTP_FORBIDDEN
            assert response[0].get_json()["error"] == "You do not have permission to perform this action"


def test_role_required_no_role(app):
    with app.app_context():
        mock_function = MagicMock(return_value=(jsonify({"message": "success"}), HTTP_OK))

        mock_user = MagicMock()
        mock_user.role = None

        with (
            patch("app.authz.decorators.get_jwt_identity", return_value=1),
            patch("app.authz.decorators.User.query") as mock_query,
        ):
            mock_query.get.return_value = mock_user

            decorated_function = role_required(["admin"])(mock_function)

            response = decorated_function()
            assert response[1] == HTTP_FORBIDDEN
            assert response[0].get_json()["error"] == "You do not have permission to perform this action"
