from uuid import uuid4

import pytest
from fastapi import HTTPException

from domain.models.user import User, UserRole
from infrastructure.security.admin_access import require_admin


@pytest.mark.asyncio
async def test_require_admin_returns_admin_user():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    result = await require_admin(user)

    assert result == user

@pytest.mark.asyncio
async def test_require_admin_rejects_artist():
    user = User(
        id=uuid4(),
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=uuid4(),
    )

    with pytest.raises(HTTPException) as exc_info:
        await require_admin(user)

    assert exc_info.value.status_code == 403