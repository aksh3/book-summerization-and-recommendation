from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

# Sync stack (used for migrations and admin tasks)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

# Async stack (used in service functions and async routes)
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
async_engine = create_async_engine(DATABASE_URL, echo=True)
def get_async_session():
    return sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
async_session = get_async_session()
