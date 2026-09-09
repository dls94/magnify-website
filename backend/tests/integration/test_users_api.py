from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from domain.models.artist import Artist
from domain.models.release import Release, ReleaseType
from domain.models.user import User, UserRole
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.artist_repository import ArtistRepository
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


def test_create_user(authenticated_admin):
    email = f"new-user-{uuid4()}@magnify.music"

    response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["role"] == "ADMIN"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data

def test_create_artist_user_requires_artist_id(authenticated_admin):
    response = client.post(
        "/api/v1/users",
        json={
            "email": f"artist-{uuid4()}@magnify.music",
            "password": "password123",
            "role": "ARTIST",
        },
    )

    assert response.status_code == 400
    assert "doit être associé" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_artist_user_with_artist_id(authenticated_admin):
    artist_id = uuid4()
    email = f"artist-{uuid4()}@magnify.music"

    artist = Artist(
        id=artist_id,
        name=f"Test Artist {uuid4()}",
    )

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)
        await repository.save(artist)

    response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ARTIST",
            "artist_id": str(artist_id),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["role"] == "ARTIST"
    assert data["artist_id"] == str(artist_id)

def test_list_users(authenticated_admin):
    response = client.get("/api/v1/users")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_list_users_returns_users(authenticated_admin):
    email = f"listed-user-{uuid4()}@magnify.music"

    response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert response.status_code == 201

    response = client.get("/api/v1/users")

    assert response.status_code == 200

    data = response.json()

    assert any(user["email"] == email for user in data)


def test_get_user(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == email
    assert data["role"] == "ADMIN"

def test_get_user_not_found(authenticated_admin):
    user_id = uuid4()

    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Utilisateur introuvable."

def test_update_user(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"
    updated_email = f"updated-{uuid4()}@magnify.music"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "email": updated_email,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == updated_email
    assert data["role"] == "ADMIN"

def test_update_user_to_artist_requires_artist_id(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "role": "ARTIST",
        },
    )

    assert response.status_code == 400
    assert "doit être associé" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_user_to_artist_with_artist_id(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"
    artist_id = uuid4()

    artist = Artist(
        id=artist_id,
        name=f"Test Artist {uuid4()}",
    )

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)
        await repository.save(artist)

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "role": "ARTIST",
            "artist_id": str(artist_id),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["role"] == "ARTIST"
    assert data["artist_id"] == str(artist_id)

@pytest.mark.asyncio
async def test_update_artist_user_to_admin_clears_artist_id(authenticated_admin):
    artist_id = uuid4()
    email = f"artist-{uuid4()}@magnify.music"

    artist = Artist(
        id=artist_id,
        name=f"Test Artist {uuid4()}",
    )

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)
        await repository.save(artist)

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ARTIST",
            "artist_id": str(artist_id),
        },
    )

    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "role": "ADMIN",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["role"] == "ADMIN"
    assert data["artist_id"] is None

def test_delete_user(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/users/{user_id}")

    assert get_response.status_code == 404

def test_delete_user_not_found(authenticated_admin):
    user_id = uuid4()

    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Utilisateur introuvable."

@pytest.fixture
def authenticated_artist():
    artist = User(
        email=f"artist-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    async def fake_authenticated_user() -> User:
        return artist

    app.dependency_overrides[get_authenticated_user] = fake_authenticated_user

    yield artist

    app.dependency_overrides.clear()

def test_artist_cannot_list_users(authenticated_artist):
    response = client.get("/api/v1/users")

    assert response.status_code == 403
    assert response.json()["detail"] == "Accès administrateur requis."

@pytest.mark.parametrize(
    ("method", "path", "payload"),
    [
        ("get", "/api/v1/users", None),
        ("get", "/api/v1/users/{user_id}", None),
        ("patch", "/api/v1/users/{user_id}", {"email": "updated@magnify.music"}),
        ("delete", "/api/v1/users/{user_id}", None),
        (
            "post",
            "/api/v1/users",
            {
                "email": "user@magnify.music",
                "password": "password123",
                "role": "ADMIN",
            },
        ),
    ],
)
def test_artist_cannot_manage_users(
    authenticated_artist,
    method,
    path,
    payload,
):
    user_id = uuid4()

    if "{user_id}" in path:
        path = path.replace("{user_id}", str(user_id))

    request = getattr(client, method)

    if payload is None:
        response = request(path)
    else:
        response = request(path, json=payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Accès administrateur requis."

@pytest.mark.asyncio
async def test_artist_can_get_own_artist(authenticated_artist):
    artist = Artist(
        id=authenticated_artist.artist_id,
        name=f"Test Artist {uuid4()}",
    )

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)
        await repository.save(artist)

    response = client.get("/api/v1/me/artist")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(authenticated_artist.artist_id)
    assert data["name"] == artist.name

@pytest.mark.asyncio
async def test_artist_can_get_own_releases(authenticated_artist):
    own_artist = Artist(
        id=authenticated_artist.artist_id,
        name=f"Own Artist {uuid4()}",
    )
    other_artist = Artist(
        id=uuid4(),
        name=f"Other Artist {uuid4()}",
    )

    own_release = Release(
        title=f"Own Release {uuid4()}",
        release_type=ReleaseType.ALBUM,
        release_date=datetime.now(UTC).date(),
        artist_id=own_artist.id,
    )
    other_release = Release(
        title=f"Other Release {uuid4()}",
        release_type=ReleaseType.SINGLE,
        release_date=datetime.now(UTC).date(),
        artist_id=other_artist.id,
    )

    async with AsyncSessionLocal() as session:
        artist_repository = ArtistRepository(session)
        release_repository = ReleaseRepository(session)

        await artist_repository.save(own_artist)
        await artist_repository.save(other_artist)
        await release_repository.save(own_release)
        await release_repository.save(other_release)

    response = client.get("/api/v1/me/releases")

    assert response.status_code == 200
    data = response.json()

    release_ids = {item["id"] for item in data}

    assert str(own_release.id) in release_ids
    assert str(other_release.id) not in release_ids

@pytest.mark.asyncio
async def test_admin_gets_no_current_artist_releases(authenticated_admin):
    response = client.get("/api/v1/me/releases")

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_artist_cannot_update_another_artist_release(authenticated_artist):
    own_artist = Artist(
        id=authenticated_artist.artist_id,
        name=f"Own Artist {uuid4()}",
    )
    other_artist = Artist(
        id=uuid4(),
        name=f"Other Artist {uuid4()}",
    )

    other_release = Release(
        title=f"Other Release {uuid4()}",
        release_type=ReleaseType.ALBUM,
        release_date=datetime.now(UTC).date(),
        artist_id=other_artist.id,
    )

    async with AsyncSessionLocal() as session:
        artist_repository = ArtistRepository(session)
        release_repository = ReleaseRepository(session)

        await artist_repository.save(own_artist)
        await artist_repository.save(other_artist)
        await release_repository.save(other_release)

    response = client.patch(
        f"/api/v1/releases/{other_release.id}",
        json={"title": "Hacked Release"},
    )

    assert response.status_code == 403

def test_create_user_with_duplicate_email_returns_409(authenticated_admin):
    email = f"duplicate-{uuid4()}@magnify.music"

    payload = {
        "email": email,
        "password": "password123",
        "role": "ADMIN",
    }

    first_response = client.post(
        "/api/v1/users",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/users",
        json=payload,
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Un utilisateur avec cet email existe déjà."
    )

def test_update_user_with_duplicate_email_returns_409(authenticated_admin):
    first_email = f"first-{uuid4()}@magnify.music"
    second_email = f"second-{uuid4()}@magnify.music"

    first_response = client.post(
        "/api/v1/users",
        json={
            "email": first_email,
            "password": "password123",
            "role": "ADMIN",
        },
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/users",
        json={
            "email": second_email,
            "password": "password123",
            "role": "ADMIN",
        },
    )
    assert second_response.status_code == 201

    second_user_id = second_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{second_user_id}",
        json={
            "email": first_email,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Un utilisateur avec cet email existe déjà."
    )

def test_delete_artist_returns_409_when_referenced_by_release(
    authenticated_admin,
):
    artist = Artist(name="Referenced Artist")

    import asyncio

    async def save_artist() -> None:
        async with AsyncSessionLocal() as session:
            repository = ArtistRepository(session)
            await repository.save(artist)

    asyncio.run(save_artist())

    release = Release(
        title="Referenced Release",
        release_type=ReleaseType.SINGLE,
        release_date=datetime.now(UTC).date(),
        artist_id=artist.id,
    )

    async def save_release() -> None:
        async with AsyncSessionLocal() as session:
            repository = ReleaseRepository(session)
            await repository.save(release)

    asyncio.run(save_release())

    with TestClient(app) as client:
        response = client.delete(
            f"/api/v1/artists/{artist.id}",
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Impossible de supprimer un artiste associé à des données existantes."
    }

def test_create_user_rejects_blank_password(authenticated_admin):
    response = client.post(
        "/api/v1/users",
        json={
            "email": f"user-{uuid4()}@magnify.music",
            "password": "",
            "role": "ADMIN",
        },
    )

    assert response.status_code == 422

def test_create_user_rejects_invalid_email(authenticated_admin):
    response = client.post(
        "/api/v1/users",
        json={
            "email": "not-an-email",
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert response.status_code == 422

def test_update_user_rejects_invalid_email(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={"email": "not-an-email"},
    )

    assert response.status_code == 422

def test_update_user_rejects_blank_email(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={"email": ""},
    )

    assert response.status_code == 422

def test_update_user_accepts_empty_payload(authenticated_admin):
    email = f"user-{uuid4()}@magnify.music"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": "password123",
            "role": "ADMIN",
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={},
    )

    assert response.status_code == 200
    assert response.json()["email"] == email