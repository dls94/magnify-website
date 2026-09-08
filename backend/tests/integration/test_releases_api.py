from datetime import date
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from domain.models.release import Release, ReleaseType
from domain.models.user import User, UserRole
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.release_repository import ReleaseRepository
from infrastructure.security.dependencies import get_authenticated_user
from main import app

client = TestClient(app)

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

def test_artist_cannot_create_release():
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
        response = client.post(
            "/api/v1/releases",
            json={
                "title": "Forbidden Release",
                "artist_id": None,
                "release_type": "SINGLE",
                "release_date": "2026-09-01",
            },
        )

        assert response.status_code == 403
        assert response.json() == {
            "detail": "Accès administrateur requis."
        }
    finally:
        app.dependency_overrides.clear()

def test_create_release(authenticated_admin):
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

async def test_get_release():
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url="https://example.com/cover.jpg",
    )

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        await repository.save(release)

    response = client.get(f"/api/v1/releases/{release.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(release.id)
    assert data["title"] == "Echo Urbain"
    assert data["release_type"] == "SINGLE"
    assert data["release_date"] == "2026-09-01"
    assert data["cover_url"] == "https://example.com/cover.jpg"

def test_get_release_returns_404_when_not_found():
    response = client.get("/api/v1/releases/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Release not found"}

async def test_list_releases():
    releases = [
        Release(
            title="Echo Urbain",
            release_type=ReleaseType.SINGLE,
            release_date=date(2026, 9, 1),
            cover_url="https://example.com/echo.jpg",
        ),
        Release(
            title="Nuits Magnify",
            release_type=ReleaseType.EP,
            release_date=date(2026, 10, 1),
            cover_url="https://example.com/nuits.jpg",
        ),
    ]

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)

        for release in releases:
            await repository.save(release)

    response = client.get("/api/v1/releases")

    assert response.status_code == 200

    data = response.json()

    returned_ids = {item["id"] for item in data}

    assert str(releases[0].id) in returned_ids
    assert str(releases[1].id) in returned_ids

async def test_update_release(authenticated_admin):
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url="https://example.com/cover.jpg",
        upc="123456789",
        spotify_url="https://open.spotify.com/album/test",
    )

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        await repository.save(release)

    response = client.patch(
        f"/api/v1/releases/{release.id}",
        json={
            "title": "Echo Urbain Deluxe",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(release.id)
    assert data["title"] == "Echo Urbain Deluxe"
    assert data["release_type"] == "SINGLE"
    assert data["release_date"] == "2026-09-01"
    assert data["cover_url"] == "https://example.com/cover.jpg"

def test_update_release_returns_404_when_not_found(authenticated_admin):
    response = client.patch(
        "/api/v1/releases/00000000-0000-0000-0000-000000000000",
        json={
            "title": "Release inexistante",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Release not found"}

async def test_update_release_rejects_blank_title(authenticated_admin):
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
    )

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        await repository.save(release)

    response = client.patch(
        f"/api/v1/releases/{release.id}",
        json={
            "title": "   ",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Le titre de la release est obligatoire."
    }

async def test_delete_release(authenticated_admin):
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
    )

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        await repository.save(release)

    response = client.delete(f"/api/v1/releases/{release.id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/api/v1/releases/{release.id}")

    assert get_response.status_code == 404

def test_delete_release_returns_404_when_not_found(authenticated_admin):
    response = client.delete(
        "/api/v1/releases/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Release not found"}

def test_artist_cannot_update_release():
    release = Release(
        title="Release To Update",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
    )

    import asyncio

    async def save_release() -> None:
        async with AsyncSessionLocal() as session:
            repository = ReleaseRepository(session)
            await repository.save(release)

    asyncio.run(save_release())

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
        response = client.patch(
            f"/api/v1/releases/{release.id}",
            json={"title": "Forbidden Update"},
        )

        assert response.status_code == 403
        assert response.json() == {
            "detail": "Accès administrateur requis."
        }
    finally:
        app.dependency_overrides.clear()


def test_artist_cannot_delete_release():
    release = Release(
        title="Release To Delete",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
    )

    import asyncio

    async def save_release() -> None:
        async with AsyncSessionLocal() as session:
            repository = ReleaseRepository(session)
            await repository.save(release)

    asyncio.run(save_release())

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
        response = client.delete(
            f"/api/v1/releases/{release.id}",
        )

        assert response.status_code == 403
        assert response.json() == {
            "detail": "Accès administrateur requis."
        }
    finally:
        app.dependency_overrides.clear()