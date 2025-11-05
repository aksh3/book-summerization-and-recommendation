from flask import jsonify, request
from sqlalchemy.future import select
from sqlalchemy import desc
from ..extensions import async_session
from ..models.book import Book
from ..models.review import Review
from ..core.llama3_client import run_llama3, generate_summary_with_ollama
from flask_jwt_extended import get_jwt_identity
import asyncio
from langchain_community.llms import Ollama

async def generate_summary(data):
    try:
        text = data.get("text")

        if not text:
            return {"msg": "Text required"}, 400

        # llm = Ollama(model="llama3")
        # response = llm.predict("Summarize this book whose content is ",text)

        # summary_content = await generate_summary_with_ollama(f"Summarize this book:\n{text}")
        llm = Ollama(model="llama3")
        summary_content = await asyncio.to_thread(llm.invoke, f"Summarize this book with maximum of 200 words whose content is:\n{text}")
        print(summary_content)

        return jsonify(summary_content)
    except Exception as e:
        print("generate_summary")
        return(e)

async def get_recommendations_for_user(args):
    try:
        # identity = get_jwt_identity()
        # user_id = identity["id"]
        user_id = 1
        async with async_session() as session:
            # Get user reviews
            result = await session.execute(select(Review).where(Review.user_id == user_id))
            user_reviews = result.scalars().all()

            if not user_reviews:
                # Recommend popular books
                result = await session.execute(
                    select(Book).order_by(desc(Book.review_count)).limit(5)
                )
                books = result.scalars().all()
                return jsonify({"recommendations": [b.title for b in books]}), 200

            # Build preference profile
            book_ids = [r.book_id for r in user_reviews]
            result = await session.execute(select(Book).where(Book.id.in_(book_ids)))
            preferred_books = result.scalars().all()

            summary_text = ". ".join([b.summary or b.title for b in preferred_books if b])
            llm = Ollama(model="llama3")
            # Use Llama3 to generate recommendations
            # prompt = f"Using the following preferred books, recommend 5 other books: {summary_text}"
            recomendations=await asyncio.to_thread(llm.invoke, f"Using the following preferred books, recommend 5 other books name with bulleted format: {summary_text}")

            return jsonify({"recommendations": recomendations}), 200
    except Exception as e:
        print("exception in get_recommendations_for_user")
        return(e)