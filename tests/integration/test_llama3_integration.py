def test_create_book(client):
    # Simulate admin login to get JWT
    resp = client.post("/api/auth/register", json={
        "username": "admin",
        "password": "adminpass"
    })
    login = client.post("/api/auth/login", json={
        "username": "admin", "password": "adminpass"
    })
    token = login.json.get("access_token")
    resp = client.post(
        "/api/books/",
        json={"title": "Book 1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    resp = client.get("/api/books/")
    assert resp.status_code == 200