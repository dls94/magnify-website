from uuid import uuid4

import pytest

from domain.models.user import User, UserRole
from infrastructure.security.current_user import get_current_user


class FakeTokenProvider:
    def __init__(self, payload: dict[str, object] | None) -> None:
        self.payload = payload

    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, object] | None:
        return self.payload


class FakeUserRepository:
    def __init__(self, user: User | None) -> None:
        self.user = user

    async def get_by_id(self, user_id):
        if self.user is not None and self.user.id == user_id:
            return self.user

        return None


@pytest.mark.asyncio
async def test_get_current_user_returns_user_from_valid_token():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    token_provider = FakeTokenProvider(
        {
            "sub": str(user.id),
            "role": "ADMIN",
        }
    )
    repository = FakeUserRepository(user)

    result = await get_current_user(
        token="valid-token",
        token_provider=token_provider,
        repository=repository,
    )

    assert result == user

@pytest.mark.asyncio
async def test_get_current_user_returns_none_for_invalid_token():
    token_provider = FakeTokenProvider(None)
    repository = FakeUserRepository(None)

    result = await get_current_user(
        token="invalid-token",
        token_provider=token_provider,
        repository=repository,
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_current_user_returns_none_when_user_does_not_exist():
    user_id = uuid4()

    token_provider = FakeTokenProvider(
        {
            "sub": str(user_id),
            "role": "ADMIN",
        }
    )
    repository = FakeUserRepository(None)

    result = await get_current_user(
        token="valid-token",
        token_provider=token_provider,
        repository=repository,
    )

    assert result is None

@pytest.mark.asyncio
async def test_get_current_user_returns_none_for_inactive_user():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
        is_active=False,
    )

    token_provider = FakeTokenProvider(
        {
            "sub": str(user.id),
            "role": "ADMIN",
        }
    )
    repository = FakeUserRepository(user)

    result = await get_current_user(
        token="valid-token",
        token_provider=token_provider,
        repository=repository,
    )

    assert result is None

@pytest.mark.asyncio
async def test_get_current_user_ignores_role_from_token():
    user = User(
        id=uuid4(),
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    token_provider = FakeTokenProvider(
        {
            "sub": str(user.id),
            "role": "ADMIN",
        }
    )
    repository = FakeUserRepository(user)

    result = await get_current_user(
        token="forged-admin-token",
        token_provider=token_provider,
        repository=repository,
    )

    assert result == user
    assert result.role == UserRole.ARTIST