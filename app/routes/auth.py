from flask import Blueprint, request, jsonify
from ..services.auth_service import (
    register_user,
    authenticate_user,
    get_current_user,
    change_password,
)
from ..utils.jwt_utils import requires_role, jwt_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
async def register():
    data = request.get_json()
    return await register_user(data)

@auth_bp.route("/login", methods=["POST"])
async def login():
    data = request.get_json()
    return await authenticate_user(data)

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
async def me():
    return await get_current_user()

@auth_bp.route("/password", methods=["PATCH"])
@jwt_required()
async def password():
    data = request.get_json()
    return await change_password(data)