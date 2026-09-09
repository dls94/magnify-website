import asyncio
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi.testclient import TestClient

from domain.models.artist import Artist
from domain.models.user import User, UserRole
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.dependencies import (
    get_authenticate_user,
    get_token_provider,
)
from infrastructure.database.repositories.artist_repository import ArtistRepository
from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.security.dependencies import get_authenticated_user
from infrastructure.security.jwt_token_provider import JwtTokenProvider
from main import app

client = TestClient(app)

class FakeAuthenticateUser:
    def __init__(self, user: User | None) -> None:
        self.user = user

    async def execute(self, email: str, password: str) -> User | None:
        if (
            self.user is not None
            and self.user.is_active
            and email == self.user.email
            and password == "correct-password"
        ):
            return self.user

        return None


class FakeTokenProvider:
    def create_access_token(
        self,
        subject: str,
        claims: dict[str, object],
    ) -> str:
        return "fake-access-token"

    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, object] | None:
        return None


def test_login_returns_access_token_for_valid_credentials():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    app.dependency_overrides[get_authenticate_user] = (
        lambda: FakeAuthenticateUser(user)
    )
    app.dependency_overrides[get_token_provider] = (
        lambda: FakeTokenProvider()
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@magnify.music",
                "password": "correct-password",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["access_token"] == "fake-access-token"
        assert data["token_type"] == "bearer"
        assert data["user"]["id"] == str(user.id)
        assert data["user"]["email"] == user.email
        assert data["user"]["role"] == "ADMIN"
    finally:
        app.dependency_overrides.clear()


def test_login_returns_401_for_invalid_credentials():
    app.dependency_overrides[get_authenticate_user] = (
        lambda: FakeAuthenticateUser(None)
    )
    app.dependency_overrides[get_token_provider] = (
        lambda: FakeTokenProvider()
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@magnify.music",
                "password": "wrong-password",
            },
        )

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()

def test_login_returns_401_for_inactive_user():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
        is_active=False,
    )

    app.dependency_overrides[get_authenticate_user] = (
        lambda: FakeAuthenticateUser(user)
    )
    app.dependency_overrides[get_token_provider] = (
        lambda: FakeTokenProvider()
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@magnify.music",
                "password": "correct-password",
            },
        )

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()

def test_get_me_returns_authenticated_user():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    app.dependency_overrides[get_authenticated_user] = lambda: user

    try:
        client = TestClient(app)

        response = client.get("/api/v1/auth/me")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(user.id)
        assert data["email"] == user.email
        assert data["role"] == "ADMIN"
    finally:
        app.dependency_overrides.clear()

def test_get_me_returns_401_without_token():
    client = TestClient(app)

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401

def test_get_me_returns_401_for_invalid_token():
    client = TestClient(app)

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401

def test_get_current_user_returns_401_for_expired_token():
    token_provider = JwtTokenProvider(
        secret_key="test-secret",
        access_token_expire_minutes=1,
    )

    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "iat": datetime.now(UTC) - timedelta(minutes=10),
            "exp": datetime.now(UTC) - timedelta(minutes=5),
        },
        "test-secret",
        algorithm="HS256",
    )

    app.dependency_overrides[get_token_provider] = lambda: token_provider

    try:
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == (
            "Token invalide ou utilisateur non authentifié."
        )
    finally:
        app.dependency_overrides.clear()

def test_get_current_user_returns_401_for_token_without_subject():
    token = jwt.encode(
        {
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "test-secret",
        algorithm="HS256",
    )

    token_provider = JwtTokenProvider(
        secret_key="test-secret",
        access_token_expire_minutes=60,
    )

    app.dependency_overrides[get_token_provider] = lambda: token_provider

    try:
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()

def test_get_current_user_returns_401_for_invalid_subject():
    token = jwt.encode(
        {
            "sub": "not-a-valid-uuid",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "test-secret",
        algorithm="HS256",
    )

    token_provider = JwtTokenProvider(
        secret_key="test-secret",
        access_token_expire_minutes=60,
    )

    app.dependency_overrides[get_token_provider] = lambda: token_provider

    try:
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()

def test_get_current_user_returns_401_for_unknown_user():
    user_id = uuid4()

    token = jwt.encode(
        {
            "sub": str(user_id),
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "test-secret",
        algorithm="HS256",
    )

    token_provider = JwtTokenProvider(
        secret_key="test-secret",
        access_token_expire_minutes=60,
    )

    app.dependency_overrides[get_token_provider] = lambda: token_provider

    try:
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()

def test_get_me_uses_user_from_database_not_token_role():
    user = User(
        id=uuid4(),
        email=f"artist-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    token = jwt.encode(
        {
            "sub": str(user.id),
            "role": "ADMIN",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "test-secret",
        algorithm="HS256",
    )

    token_provider = JwtTokenProvider(
        secret_key="test-secret",
        access_token_expire_minutes=60,
    )

    artist = Artist(
        id=user.artist_id,
        name="JWT Test Artist",
    )

    async def save_artist() -> None:
        async with AsyncSessionLocal() as session:
            repository = ArtistRepository(session)
            await repository.save(artist)

    asyncio.run(save_artist())

    async def save_user() -> None:
        async with AsyncSessionLocal() as session:
            repository = UserRepository(session)
            await repository.save(user)

    asyncio.run(save_user())

    app.dependency_overrides[get_token_provider] = lambda: token_provider

    try:
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(user.id)
        assert data["role"] == "ARTIST"
    finally:
        app.dependency_overrides.clear()