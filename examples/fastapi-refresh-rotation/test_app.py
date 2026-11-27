from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_rotation_and_reuse_detection():
    first = client.post("/login", json={"username": "ann"}).json()
    second = client.post("/refresh", json={"refresh_token": first["refresh_token"]})
    assert second.status_code == 200
    second = second.json()

    # Replaying the first (already rotated) token fails...
    assert client.post("/refresh", json={"refresh_token": first["refresh_token"]}).status_code == 401
    # ...and kills the whole family, including the newest token.
    assert client.post("/refresh", json={"refresh_token": second["refresh_token"]}).status_code == 401


def test_access_token_is_not_a_refresh_token():
    pair = client.post("/login", json={"username": "bob"}).json()
    assert client.post("/refresh", json={"refresh_token": pair["access_token"]}).status_code == 401
