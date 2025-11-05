from flask import Blueprint, request
from ..services.review_service import (
    get_review,
    create_review
)
from ..utils.jwt_utils import jwt_required

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/<int:book_id>/reviews", methods=["GET"])
async def get_review_route(book_id):
    return await get_review(book_id)

@reviews_bp.route("/<int:book_id>/reviews", methods=["POST"])
async def create_review_route(book_id):
    data = request.get_json()
    return await create_review(data)
