from uuid import uuid4

import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient

from domain.models.user import User, UserRole
from infrastructure.security.admin_access import require_admin
from infrastructure.security.dependencies import get_authenticated_user


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()

    @app.get("/admin-only")
    async def admin_only(
        current_user: User = Depends(require_admin),
    ) -> dict[str, str]:
        return {"message": "ok"}

    return app


@pytest.mark.asyncio
async def test_admin_can_access_admin_only_endpoint(app: FastAPI):
    admin = User(
        id=uuid4(),
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    async def fake_authenticated_user() -> User:
        return admin

    app.dependency_overrides[get_authenticated_user] = fake_authenticated_user

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/admin-only")

        assert response.status_code == 200
        assert response.json() == {"message": "ok"}
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_artist_cannot_access_admin_only_endpoint(app: FastAPI):
    artist = User(
        id=uuid4(),
        email=f"artist-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    async def fake_authenticated_user() -> User:
        return artist

    app.dependency_overrides[get_authenticated_user] = fake_authenticated_user

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/admin-only")

        assert response.status_code == 403
        assert response.json()["detail"] == "Accès administrateur requis."
    finally:
        app.dependency_overrides.clear()