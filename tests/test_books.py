def test_create_book(client):
    breakpoint()
    # Simulate admin login to get JWT
    resp = client.post("/auth/register", json={{
  "email": "akash1@example.com",
  "password": "secure123",
  "username": "akash1"
}
    })
    login = client.post("/auth/login", json={
        "username": "admin", "password": "adminpass"
    })
    token = login.json.get("access_token")
    resp = client.post(
        "/books/",
        json={"title": "Book 1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    resp = client.get("/api/books/")
    assert resp.status_code == 200