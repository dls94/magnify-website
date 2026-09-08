from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from domain.models.artist import Artist
from domain.models.user import User, UserRole
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.artist_repository import ArtistRepository
from infrastructure.security.dependencies import get_authenticated_user
from main import app


@pytest.fixture
def authenticated_admin():
    admin = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    async def fake_authenticated_user() -> User:
        return admin

    app.dependency_overrides[get_authenticated_user] = fake_authenticated_user

    yield admin

    app.dependency_overrides.clear()

def test_list_artists_returns_artists():
    with TestClient(app) as client:
        response = client.get("/api/v1/artists")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_artist_returns_artist():
    artist = Artist(
        name="API Artist",
        bio="Artist for API test.",
        picture_url="https://example.com/api.jpg",
    )

    # Préparation de la donnée en base
    import asyncio

    async def save_artist() -> None:
        async with AsyncSessionLocal() as session:
            repository = ArtistRepository(session)
            await repository.save(artist)

    asyncio.run(save_artist())

    with TestClient(app) as client:
        response = client.get(f"/api/v1/artists/{artist.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(artist.id)
    assert data["name"] == "API Artist"
    assert data["bio"] == "Artist for API test."
    assert data["picture_url"] == "https://example.com/api.jpg"
    assert "created_at" not in data


def test_get_artist_returns_404_when_artist_does_not_exist():
    artist_id = uuid4()

    with TestClient(app) as client:
        response = client.get(f"/api/v1/artists/{artist_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Artist not found"}

def test_create_artist_returns_created_artist(authenticated_admin):
    payload = {
        "name": "New API Artist",
        "bio": "Artist created through the API.",
        "spotify_url": "https://open.spotify.com/artist/test",
        "instagram_url": "https://instagram.com/new_api_artist",
        "picture_url": "https://example.com/new-api.jpg",
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/artists", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["bio"] == payload["bio"]
    assert data["spotify_url"] == payload["spotify_url"]
    assert data["instagram_url"] == payload["instagram_url"]
    assert data["picture_url"] == payload["picture_url"]
    assert "id" in data
    assert "created_at" not in data

def test_create_artist_persists_artist(authenticated_admin):
    payload = {
        "name": "Persisted API Artist",
        "bio": "Artist that must be persisted.",
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/artists", json=payload)

    assert response.status_code == 201

    artist_id = response.json()["id"]

    import asyncio

    async def get_artist_from_database():
        async with AsyncSessionLocal() as session:
            repository = ArtistRepository(session)
            return await repository.get_by_id(artist_id)

    artist = asyncio.run(get_artist_from_database())

    assert artist is not None
    assert str(artist.id) == artist_id
    assert artist.name == payload["name"]
    assert artist.bio == payload["bio"]

def test_create_artist_rejects_blank_name(authenticated_admin):
    payload = {
        "name": "   ",
        "bio": "Invalid artist.",
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/artists", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Le nom de l'artiste est obligatoire."
    }

def test_update_artist_returns_updated_artist(authenticated_admin):
    payload = {
        "name": "Updated API Artist",
        "bio": "Updated biography.",
        "spotify_url": "https://open.spotify.com/artist/updated",
        "instagram_url": "https://instagram.com/updated_artist",
        "picture_url": "https://example.com/updated.jpg",
    }

    with TestClient(app) as client:
        create_response = client.post(
            "/api/v1/artists",
            json={"name": "Original API Artist"},
        )

        assert create_response.status_code == 201

        artist_id = create_response.json()["id"]

        response = client.patch(
            f"/api/v1/artists/{artist_id}",
            json=payload,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == artist_id
    assert data["name"] == payload["name"]
    assert data["bio"] == payload["bio"]
    assert data["spotify_url"] == payload["spotify_url"]
    assert data["instagram_url"] == payload["instagram_url"]
    assert data["picture_url"] == payload["picture_url"]
    assert "created_at" not in data

def test_update_artist_returns_404_when_artist_does_not_exist(authenticated_admin):
    artist_id = uuid4()

    payload = {
        "name": "Updated Artist",
    }

    with TestClient(app) as client:
        response = client.patch(
            f"/api/v1/artists/{artist_id}",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Artist not found"}

def test_delete_artist_returns_no_content(authenticated_admin):
    with TestClient(app) as client:
        create_response = client.post(
            "/api/v1/artists",
            json={"name": "Artist To Delete"},
        )

        assert create_response.status_code == 201

        artist_id = create_response.json()["id"]

        response = client.delete(
            f"/api/v1/artists/{artist_id}",
        )

    assert response.status_code == 204
    assert response.content == b""

def test_delete_artist_returns_404_when_artist_does_not_exist(authenticated_admin):
    artist_id = uuid4()

    with TestClient(app) as client:
        response = client.delete(
            f"/api/v1/artists/{artist_id}",
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Artist not found"}

def test_artist_cannot_create_artist():
    artist_user = User(
        email=f"artist-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    async def fake_authenticated_user() -> User:
        return artist_user

    app.dependency_overrides[get_authenticated_user] = fake_authenticated_user

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/artists",
                json={"name": "Forbidden Artist"},
            )

        assert response.status_code == 403
        assert response.json() == {
            "detail": "Accès administrateur requis."
        }
    finally:
        app.dependency_overrides.clear()


def test_artist_cannot_update_artist():
    artist = Artist(name="Artist To Update")

    import asyncio

    async def save_artist() -> None:
        async with AsyncSessionLocal() as session:
            repository = ArtistRepository(session)
            await repository.save(artist)

    asyncio.run(save_artist())

    artist_user = User(
        email=f"artist-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    async def fake_authenticated_user() -> User:
        return artist_user

    app.dependency_overrides[get_authenticated_user] = fake_authenticated_user

    try:
        with TestClient(app) as client:
            response = client.patch(
                f"/api/v1/artists/{artist.id}",
                json={"name": "Forbidden Update"},
            )

        assert response.status_code == 403
        assert response.json() == {
            "detail": "Accès administrateur requis."
        }
    finally:
        app.dependency_overrides.clear()


def test_artist_cannot_delete_artist():
    artist = Artist(name="Artist To Delete")

    import asyncio

    async def save_artist() -> None:
        async with AsyncSessionLocal() as session:
            repository = ArtistRepository(session)
            await repository.save(artist)

    asyncio.run(save_artist())

    artist_user = User(
        email=f"artist-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    async def fake_authenticated_user() -> User:
        return artist_user

    app.dependency_overrides[get_authenticated_user] = fake_authenticated_user

    try:
        with TestClient(app) as client:
            response = client.delete(
                f"/api/v1/artists/{artist.id}",
            )

        assert response.status_code == 403
        assert response.json() == {
            "detail": "Accès administrateur requis."
        }
    finally:
        app.dependency_overrides.clear()