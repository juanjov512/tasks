import os
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_APP = os.getenv("FLASK_APP", "app.py")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_ENV") == "development"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))
    JWT_TOKEN_LOCATION: ClassVar[list[str]] = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_ERROR_MESSAGE_KEY = "msg"

    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "db")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(",")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def get_database_url(cls):
        return cls.SQLALCHEMY_DATABASE_URI

    @classmethod
    def get_jwt_config(cls):
        return {
            "secret_key": cls.JWT_SECRET_KEY,
            "access_token_expires": cls.JWT_ACCESS_TOKEN_EXPIRES,
        }


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-jwt-secret-key"
    CORS_ORIGINS: ClassVar[list[str]] = ["http://localhost:3000"]
