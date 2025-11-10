from flask import jsonify
from sqlalchemy.future import select
from sqlalchemy import func
from ..models.review import Review
from ..schemas.review import review_schema, reviews_schema
from ..models.book import Book
from ..extensions import async_session
from flask_jwt_extended import get_jwt_identity


async def get_review(book_id):
    try:
        async with async_session() as session:
            result = await session.execute(select(Review).where(Review.book_id == book_id))
            review = result.scalar_one_or_none()
            if review:
                return jsonify(review_schema.dump(review)), 200
            return {"msg": "Review not found"}, 404
    except Exception as e:
        return e


async def create_review(data):
    async with async_session() as session:
        identity = get_jwt_identity()
        data["user_id"] = identity["id"]
        review = Review(**data)
        session.add(review)
        await session.commit()
        await update_review_count(session, review.book_id)
        await session.refresh(review)
        return jsonify(review_schema.dump(review)), 201




async def update_review_count(session, book_id):
    result = await session.execute(
        select(func.count()).select_from(Review).where(Review.book_id == book_id)
    )
    count = result.scalar()
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if book:
        book.review_count = count
        await session.commit()