def test_register_and_login(client):
    resp = client.post("/auth/register", json={
        "username": "testuser",
        "password": "password"
    })
    assert resp.status_code == 201
    resp = client.post("/auth/login", json={
        "username": "testuser",
        "password": "password"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json