def test_end_to_end(client):
    # Register, login, create book, add review, generate summary, get recommendations
    client.post("/api/auth/register", json={"username": "u", "password": "p"})
    login = client.post("/api/auth/login", json={"username": "u", "password": "p"}).json
    token = login["access_token"]
    client.post("/api/books/", json={"title": "foo"}, headers={"Authorization": f"Bearer {token}"})
    b = client.get("/api/books/").json['books'][0]
    bid = b['id']
    client.post("/api/reviews/", json={"book_id": bid, "user_id": 1, "content": "Nice", "rating": 5}, headers={"Authorization": f"Bearer {token}"})
    # Simulate Llama3 integration in summary as in test_llama3_integration
    