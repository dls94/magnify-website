from datetime import date

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_release():
    response = client.post(
        "/api/v1/releases",
        json={
            "title": "Echo Urbain",
            "artist_id": None,
            "release_type": "SINGLE",
            "release_date": "2026-09-01",
            "cover_url": "https://example.com/cover.jpg",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["title"] == "Echo Urbain"
    assert data["artist_id"] is None
    assert data["release_type"] == "SINGLE"
    assert data["release_date"] == "2026-09-01"
    assert data["cover_url"] == "https://example.com/cover.jpg"