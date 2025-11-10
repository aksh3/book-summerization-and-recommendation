import pytest
from app.extensions import async_session
from app.models.book import Book
from app.models.review import Review


@pytest.mark.asyncio
async def test_get_reviews_empty(client):
    """Should return empty reviews list for a book that has none."""

    # Create a book in DB
    async with async_session() as session:
        async with session.begin():
            session.add(Book(
                id=42,
                author="Chimamanda Ngozi Adichie",
                genre= "Literary Fiction",
            summary= "A powerful coming-of-age novel exploring identity, immigration, and the complexities of family ties.",
            title= "Americanah",
            year_published= 2013
            ))
    resp = await client.get("/books/1/reviews")
    assert resp.status_code == 404
    assert resp.json() == {'msg': 'Review not found'}

@pytest.mark.no_db_clean
@pytest.mark.asyncio
async def test_create_review(client,admin_token):
    """Should create a review for a book."""

    data = {
  "book_id": 42,
  "id": 42,
  "rating": 5,
  "review_text": "A deeply engaging read — well paced, emotionally resonant, and full of memorable characters. Recommended for readers who enjoy character-driven contemporary fiction.",
}
    resp = await client.post("/books/1/reviews", json=data,headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 201

    output = resp.json()
    assert output["review_text"] == "A deeply engaging read — well paced, emotionally resonant, and full of memorable characters. Recommended for readers who enjoy character-driven contemporary fiction."
    assert output["rating"] == 5

@pytest.mark.no_db_clean
@pytest.mark.asyncio
async def test_get_reviews_after_creation(client):
    """Should return one review after creation."""
    breakpoint()
    resp = await client.get("/books/42/reviews")
    assert resp.status_code == 200
    reviews = resp.json()

    assert len(reviews) == 3
    assert reviews["review_text"] == "A deeply engaging read — well paced, emotionally resonant, and full of memorable characters. Recommended for readers who enjoy character-driven contemporary fiction."

