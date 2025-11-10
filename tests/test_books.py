import pytest
from app.extensions import async_session
from app.models.book import Book


@pytest.mark.asyncio
async def test_list_books_empty(client):
    resp = await client.get("/books/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_book(client, admin_token):
    data = {
  "author": "Chimamanda Ngozi Adichie",
  "genre": "Literary Fiction",
  "id": 1,
  "summary": "A powerful coming-of-age novel exploring identity, immigration, and the complexities of family ties.",
  "title": "Americanah",
  "year_published": 2013}
    resp = await client.post("/books/",json=data,headers={"Authorization": f"Bearer {admin_token}"})

    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Americanah"
    assert body["author"] == "Chimamanda Ngozi Adichie"

@pytest.mark.no_db_clean
@pytest.mark.asyncio
async def test_list_books_after_creation(client):
    resp = await client.get("/books/")
    assert resp.status_code == 200
    data = resp.json()

    assert len(data) == 1
    assert data[0]["title"] == "Americanah"

@pytest.mark.no_db_clean
@pytest.mark.asyncio
async def test_get_book(client):
    resp = await client.get("/books/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Americanah"

@pytest.mark.no_db_clean
@pytest.mark.asyncio
async def test_update_book(client, admin_token):
    update = {
  "author": "Updated Author",
  "genre": "Literary Fiction",
  "id": 1,
  "summary": "A powerful coming-of-age novel exploring identity, immigration, and the complexities of family ties.",
  "title": "Updated Title",
  "year_published": 2013}

    resp = await client.put(
        "/books/1",
        json=update,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"

@pytest.mark.no_db_clean
@pytest.mark.asyncio
async def test_delete_book(client, admin_token):
    resp = await client.delete(
        "/books/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_get_deleted_book(client):
    resp = await client.get("/books/1")
    assert resp.status_code == 404
    assert resp.json()["msg"] == "Book not found"
