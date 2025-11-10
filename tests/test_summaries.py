import pytest


@pytest.mark.asyncio
async def test_generate_summary(client, admin_token):
    """POST /generate-summary should call generate_summary() and return a summary."""

    payload = {
        "text": """Mira found the map folded inside an old library book, its edges browned like dried leaves. She had come to the town to teach for a year and left a different life behind—a job with deadlines, an apartment that hummed with loneliness. The map promised an unnamed place at the edge of the marsh, marked only by a tiny star. On Saturday she walked there, boots sinking into reed-soft earth, the sky the color of pewter.
At the marsh’s lip she discovered a door set into the ground, iron-ring cold against her palm. It opened to a narrow staircase, and a warm, dim light guided her down. Below, a room smelled of cedar and honey; shelves curved around the walls, full of notebooks and jars of paper boats. An old woman with silver hair smiled without surprise. “We collect things people think they’ve lost,” she said.
Mira handed over a cardboard box of crumpled bills, unopened letters, a rusting watch—tokens of past choices. In exchange, the woman offered a small book bound in blue thread. Inside were pages of future mornings: sounds she had forgotten, recipes she would teach, names she would say aloud. When Mira climbed back to daylight, the town felt new. She tucked the blue book into her bag and began to write.
"""
    }

    resp = await client.post(
        "/generate-summary",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert resp.status_code == 200

    data = resp.json()
    # Adjust expected keys based on your generate_summary output
    assert "summary" in data


@pytest.mark.asyncio
async def test_generate_summary_requires_auth(client):
    """Should return 401 without JWT."""
    resp = await client.post("/generate-summary", json={"text": "hello"})
    assert resp.status_code == 401   # unauthorized