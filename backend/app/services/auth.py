from datetime import UTC, datetime
from typing import Any

from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import db
from app.models import User
from app.schemas.auth import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)


class AuthService:
    @staticmethod
    def register_user(data: dict[str, Any]) -> UserResponse:
        try:
            user_data = UserCreate(**data)

            if User.query.filter_by(email=user_data.email).first():
                raise ValueError("Email already registered")

            user = User(email=user_data.email, username=user_data.username)
            user.set_password(user_data.password)

            db.session.add(user)
            db.session.commit()

            return UserResponse.model_validate(user)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def login_user(data: dict[str, Any]) -> TokenResponse:
        try:
            login_data = UserLogin(**data)

            user = User.query.filter_by(email=login_data.email).first()
            if not user or not user.check_password(login_data.password):
                raise ValueError("Invalid credentials")

            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"email": user.email, "username": user.username},
            )
            refresh_token = create_refresh_token(identity=str(user.id))

            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                email=user.email,
                user_id=user.id,
                username=user.username,
            )
        except Exception as e:
            raise ValueError(str(e)) from e

    @staticmethod
    def get_user_profile(user_id: int) -> UserResponse:
        try:
            user = User.query.get_or_404(user_id)
            return UserResponse.model_validate(user)
        except Exception as e:
            raise ValueError(str(e)) from e

    @staticmethod
    def update_user_profile(user_id: int, data: dict[str, Any]) -> UserResponse:
        try:
            update_data = UserUpdate(**data)

            user = User.query.get_or_404(user_id)

            if update_data.email and update_data.email != user.email:
                if User.query.filter_by(email=update_data.email).first():
                    raise ValueError("User email already registered")
                user.email = update_data.email

            if update_data.username:
                user.username = update_data.username

            if update_data.password is not None:
                user.set_password(update_data.password)

            user.updated_at = datetime.now(UTC)
            db.session.commit()

            return UserResponse.model_validate(user)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e
