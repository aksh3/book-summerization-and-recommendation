import pytest
from app.extensions import async_session
from app.models.review import Review
@pytest.mark.asyncio
async def test_recommendations(client, admin_token):
    """GET /recommendations should return recommendations for the user."""
    async with async_session() as session:
        async with session.begin():
            session.add(Review(
                book_id= 42,
                id= 42,
                rating= 5,
                review_text= "A deeply engaging read — well paced, emotionally resonant, and full of memorable characters. Recommended for readers who enjoy character-driven contemporary fiction.",
            user_id=1))
    resp = await client.get(
        "/recommendations",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert resp.status_code == 200
    data = resp.json()
    # Adjust based on the shape of your recommendation response
    assert isinstance(data, list) or isinstance(data, dict)


@pytest.mark.asyncio
async def test_recommendations_requires_auth(client):
    """Should return 401 without JWT."""
    resp = await client.get("/recommendations")
    assert resp.status_code == 401