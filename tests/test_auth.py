def test_register_and_login(client):
    resp = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "password"
    })
    assert resp.status_code == 201
    resp = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json