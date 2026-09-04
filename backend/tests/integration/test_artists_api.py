from fastapi.testclient import TestClient

from main import app


def test_list_artists_returns_artists():
    with TestClient(app) as client:
        response = client.get("/api/v1/artists")

    assert response.status_code == 200
    assert isinstance(response.json(), list)