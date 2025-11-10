# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

# internal storage (real engine + sessionmaker)
_async_engine = None
_async_sessionmaker = None

# INTERNAL STORAGE (DO NOT IMPORT DIRECTLY)
_async_engine = None
_async_sessionmaker = None


def get_async_engine():
    """
    Safe accessor for the async engine.
    Returns the initialized async engine.
    """
    if _async_engine is None:
        raise RuntimeError("Async engine not initialized. Call init_async_db() first.")
    return _async_engine


def async_session():
    """
    Safe accessor that returns a new AsyncSession each call.
    """
    if _async_sessionmaker is None:
        raise RuntimeError("async_session() called before init_async_db().")
    return _async_sessionmaker()

def async_session():
    """
    Safe accessor for async sessions.
    - Always returns a session, even if imported early.
    - If engine isn't initialized yet, raises a clean error.
    """
    if _async_sessionmaker is None:
        raise RuntimeError(
            "async_session() called before init_async_db(). "
            "Ensure create_app() or test fixture calls init_async_db() first."
        )
    return _async_sessionmaker()


def init_async_db(database_url: str, *, echo: bool = False):
    """Initialize async SQLAlchemy engine + sessionmaker."""
    global _async_engine, _async_sessionmaker

    print(f"[init_async_db] Initializing async DB at: {database_url}")

    _async_engine = create_async_engine(
        database_url,
        echo=echo,
        future=True,
    )

    _async_sessionmaker = sessionmaker(
        bind=_async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    print(f"[init_async_db] async_engine initialized: {_async_engine}")
    print(f"[init_async_db] async_sessionmaker initialized: {_async_sessionmaker}")


# expose for tests
async_engine = property(lambda: _async_engine)
async_sessionmaker = property(lambda: _async_sessionmaker)
