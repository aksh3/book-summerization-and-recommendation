from flask import jsonify
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from ..models.book import Book
from ..schemas.book import book_schema, books_schema
from ..extensions import async_session

async def get_books(args):
    try:
        async with async_session() as session:
            result = await session.execute(select(Book))
            books = result.scalars().all()
            return jsonify(books_schema.dump(books)), 200
    except Exception as e:
        print("get_books")
        return(e)

async def get_book(book_id):
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if book:
            return jsonify(book_schema.dump(book)), 200
        return {"msg": "Book not found"}, 404

async def create_book(data):
    async with async_session() as session:
        book = Book(**data)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return jsonify(book_schema.dump(book)), 201


async def update_book(book_id, data):
    try:
        async with async_session() as session:
            result = await session.execute(select(Book).where(Book.id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                return {"msg": "Book not found"}, 404
            for k, v in data.items():
                setattr(book, k, v)
            await session.commit()
            await session.refresh(book)
            return jsonify(book_schema.dump(book)), 200
    except Exception as e:
        print("update_book")
        return(e)


async def delete_book(book_id):
    try:
        async with async_session() as session:
            result = await session.execute(select(Book).where(Book.id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                return {"msg": "Book not found"}, 404
            await session.delete(book)
            await session.commit()
            return {}, 204
    except Exception as e:
        print("delete_book")
        return(e)