import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "changeme-supersecret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:Postgres@db:5432/bookdb"
    )
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Postgres@localhost:5432/bookdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "3892268b9c904d70900d35556a12b9417076087e620a77c4fe243830d3d9eaf1")
    OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")
    LLAMA3_MODEL = os.environ.get("LLAMA3_MODEL", "llama3")
    JWT_IDENTITY_CLAIM = "identity"
    SWAGGER = {
        'title': "Bookman API",
        'uiversion': 3,
        'openapi': '3.0.2'
    }