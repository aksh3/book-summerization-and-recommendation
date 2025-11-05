from flask import Blueprint, request
from ..services.book_service import (
    get_books,
    get_book,
    create_book,
    update_book,
    delete_book,
)
from ..utils.jwt_utils import jwt_required, requires_role

books_bp = Blueprint("books", __name__)

@books_bp.route("/", methods=["GET"])
async def list_books():
    args = request.args
    return await get_books(args)

@books_bp.route("/<int:book_id>", methods=["GET"])
async def get_book_route(book_id):
    return await get_book(book_id)

@books_bp.route("/", methods=["POST","OPTIONS"])
@jwt_required()
async def create_book_route():
    data = request.get_json()
    return await create_book(data)

@books_bp.route("/<int:book_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
async def update_book_route(book_id):
    data = request.get_json()
    return await update_book(book_id, data)

@books_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
async def delete_book_route(book_id):
    return await delete_book(book_id)