# tests/conftest.py
import os
import sys

# ✅ Ensure project root is on PYTHONPATH (needed on Windows)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import asyncio
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from asgiref.wsgi import WsgiToAsgi

from app.main import create_app
from app.extensions import db, init_async_db, get_async_engine, async_session


class TestConfig:
    """Test-only config that overrides production settings."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///./sync_test.db"
    ASYNC_DATABASE_URI = "sqlite+aiosqlite:///./async_test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "testsecret"


@pytest.fixture(scope="session")
def app():
    """Create the Flask application with TestConfig for ALL tests."""
    app = create_app()

    # ✅ Load test configuration
    app.config.from_object(TestConfig)

    # ✅ Initialize async DB with SQLite
    init_async_db(app.config["ASYNC_DATABASE_URI"])

    # ✅ Create async tables once at session start
    async def init_models():
        engine = get_async_engine()
        async with engine.begin() as conn:
            await conn.run_sync(db.metadata.create_all)

    asyncio.run(init_models())

    return app


@pytest_asyncio.fixture
async def client(app):
    """Async HTTP client for all tests."""
    asgi_app = WsgiToAsgi(app)
    transport = ASGITransport(app=asgi_app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True)
async def clean_db(request):
    # ✅ Skip DB cleanup if test has marker: @pytest.mark.no_db_clean
    if request.node.get_closest_marker("no_db_clean"):
        yield
        return

    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.drop_all)
        await conn.run_sync(db.metadata.create_all)
    yield

@pytest.fixture
def admin_token(app):
    from flask_jwt_extended import create_access_token
    with app.app_context():
        return create_access_token(identity={
            "id": 1,
            "roles": ["user"]
        })
