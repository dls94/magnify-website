from uuid import uuid4

from fastapi.testclient import TestClient

from domain.models.user import User, UserRole
from infrastructure.database.dependencies import (
    get_authenticate_user,
    get_token_provider,
)
from infrastructure.security.dependencies import get_authenticated_user
from main import app


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