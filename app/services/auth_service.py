from flask import jsonify
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from ..models.user import User, Role
from ..extensions import async_session
from ..utils.hashing import verify_password, hash_password
from flask_jwt_extended import create_access_token, get_jwt_identity

async def register_user(data):
    try:
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username or not password:
            return {"msg": "Missing username or password"}, 400

        async with async_session() as session:
            result = await session.execute(select(Role).where(Role.name == "user"))
            role = result.scalar_one_or_none()

            user = User(username=username, email=email, password_hash=hash_password(password))
            user.roles = [role] if role else []

            try:
                session.add(user)
                await session.commit()
                return {"msg": "User registered successfully"}, 201
            except IntegrityError:
                await session.rollback()
                return {"msg": "Username or email already exists"}, 409
    except Exception as e:
        print("register_user")
        return(e)

async def authenticate_user(data):
    try:
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        async with async_session() as session:
            result = await session.execute(
                select(User).options(selectinload(User.roles)).where(
                    or_(User.username == username, User.email == email)
                )
            )
            user = result.scalar_one_or_none()

            if user and verify_password(password, user.password_hash):
                roles = [role.name for role in user.roles]
                access_token = create_access_token(
                    identity={"id": user.id, "username": user.username, "roles": roles}
                )
                return {"access_token": access_token, "roles": roles}, 200
            else:
                return {"msg": "Invalid username or password"}, 401
    except Exception as e:
        print("authenticate_user error:", e)
        return {"error": str(e)}, 500

async def get_current_user():
    identity = get_jwt_identity()
    return {"user": identity}, 200

async def change_password(data):
    try:
        identity = get_jwt_identity()
        user_id = identity["id"]

        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return {"msg": "User not found"}, 404

            cur_password = data.get("current_password")
            new_password = data.get("new_password")

            if not verify_password(cur_password, user.password_hash):
                return {"msg": "Current password incorrect"}, 401

            user.password_hash = hash_password(new_password)
            await session.commit()
            return {"msg": "Password changed"}, 200
    except Exception as e:
        print("authenticate_user")
        return(e)