# app/config.py
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "changeme-supersecret")

    # ✅ Sync SQLAlchemy DB (Flask SQLAlchemy uses this)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL_SYNC",
        "postgresql://postgres:Postgres@localhost:5432/bookdb"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Async SQLAlchemy DB (asyncpg)
    ASYNC_DATABASE_URI = os.environ.get(
        "DATABASE_URL_ASYNC",
        "postgresql+asyncpg://postgres:Postgres@localhost:5432/bookdb"
    )

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret")

    OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")
    LLAMA3_MODEL = os.environ.get("LLAMA3_MODEL", "llama3")

    JWT_IDENTITY_CLAIM = "identity"

    SWAGGER = {
        "title": "Bookman API",
        "uiversion": 3,
        "openapi": "3.0.2"
    }
