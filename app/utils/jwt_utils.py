from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
import asyncio

def jwt_required():
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            return await fn(*args, **kwargs)
        return wrapper
    return decorator

def requires_role(role_name):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if role_name not in identity.get("roles", []):
                return jsonify({"msg": "Forbidden, incorrect role"}), 403
            return await fn(*args, **kwargs)
        return wrapper
    return decorator