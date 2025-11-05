from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def jwt_required():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def requires_role(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if role_name not in identity['roles']:
                from flask import jsonify
                return jsonify({"msg": "Forbidden, incorrect role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator