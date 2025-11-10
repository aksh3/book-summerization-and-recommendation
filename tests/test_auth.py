# tests/test_auth.py
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgiref.wsgi import WsgiToAsgi

from app.main import create_app
from app.extensions import db, init_async_db, get_async_engine, async_session
import app.extensions as extensions
from app.models import User
from app.utils.hashing import hash_password


@pytest.fixture(scope="module")
def app():
    app = create_app()

    # ✅ override both sync + async DBs for testing
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///./sync_test.db",
        ASYNC_DATABASE_URI="sqlite+aiosqlite:///./async_test.db",
        JWT_SECRET_KEY="testsecret",
    )

    # ✅ reinitialize async DB
    init_async_db(app.config["ASYNC_DATABASE_URI"])

    # ✅ create async tables
    async def init_models():
        engine = get_async_engine()
        async with engine.begin() as conn:
            await conn.run_sync(db.metadata.create_all)

    asyncio.run(init_models())
    return app


@pytest_asyncio.fixture
async def client(app):
    """Async client using ASGI wrapper"""
    asgi_app = WsgiToAsgi(app)
    transport = ASGITransport(app=asgi_app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    """Reset DB between tests"""
    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.drop_all)
        await conn.run_sync(db.metadata.create_all)
    yield


@pytest.mark.asyncio
async def test_login_success(app, client):
    async with async_session() as session:     # ✅ fixed
        async with session.begin():
            session.add(User(
                username="testuser",
                email="test@example.com",
                password_hash=hash_password("password123"),
            ))

    response = await client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_invalid_password(app, client):
    async with async_session() as session:     # ✅ fixed
        async with session.begin():
            session.add(User(
                username="wronguser",
                email="wrong@example.com",
                password_hash=hash_password("password123"),
            ))

    response = await client.post("/api/auth/login", json={
        "username": "wronguser",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    assert response.json()["msg"] == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_nonexistent_user(app, client):
    response = await client.post("/api/auth/login", json={
        "username": "ghost",
        "password": "nope"
    })

    assert response.status_code == 401
    assert response.json()["msg"] == "Invalid username or password"
