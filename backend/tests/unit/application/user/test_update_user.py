from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.exceptions import ArtistNotFoundError
from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.user_repository import UserRepositoryPort
from application.use_cases.user.update_user import UpdateUser
from domain.models.artist import Artist
from domain.models.user import User, UserRole
from tests.fakes.user_repository import InMemoryUserRepository


async def test_update_user():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    user = User(
        email="admin@magnify.music",
        password_hash="hash",
    )
    await repository.save(user)

    use_case = UpdateUser(repository, artist_repository)

    updated_user = await use_case.execute(
        user.id,
        email="new-admin@magnify.music",
        role=UserRole.ADMIN,
        is_active=False,
    )

    assert updated_user is user
    assert updated_user.email == "new-admin@magnify.music"
    assert updated_user.role == UserRole.ADMIN
    assert updated_user.is_active is False


async def test_update_user_returns_none_when_not_found():
    from uuid import uuid4

    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)
    use_case = UpdateUser(repository, artist_repository)

    result = await use_case.execute(
        uuid4(),
        email="admin@magnify.music",
    )

    assert result is None


async def test_update_user_rejects_blank_email():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    user = User(
        email="admin@magnify.music",
        password_hash="hash",
    )
    await repository.save(user)

    use_case = UpdateUser(repository, artist_repository)

    import pytest

    with pytest.raises(ValueError, match="L'email est obligatoire"):
        await use_case.execute(user.id, email="   ")

async def test_update_user_to_artist_requires_artist_id():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )
    await repository.save(user)

    use_case = UpdateUser(repository, artist_repository)

    with pytest.raises(ValueError, match="doit être associé"):
        await use_case.execute(
            user_id=user.id,
            role=UserRole.ARTIST,
        )

async def test_update_user_to_artist_with_artist_id():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_id = uuid4()

    artist_repository.get_by_id.return_value = Artist(
        id=artist_id,
        name="Test Artist",
    )

    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )
    await repository.save(user)

    use_case = UpdateUser(repository, artist_repository)

    updated = await use_case.execute(
        user_id=user.id,
        role=UserRole.ARTIST,
        artist_id=artist_id,
        artist_id_provided=True,
    )

    assert updated is not None
    assert updated.role == UserRole.ARTIST
    assert updated.artist_id == artist_id

async def test_update_artist_user_to_admin_clears_artist_id():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)
    artist_id = uuid4()

    user = User(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )
    await repository.save(user)

    use_case = UpdateUser(repository, artist_repository)

    updated = await use_case.execute(
        user_id=user.id,
        role=UserRole.ADMIN,
    )

    assert updated is not None
    assert updated.role == UserRole.ADMIN
    assert updated.artist_id is None

async def test_update_artist_user_without_artist_id_keeps_existing_artist_id():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)
    artist_id = uuid4()

    user = User(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )
    await repository.save(user)

    use_case = UpdateUser(repository, artist_repository)

    updated = await use_case.execute(
        user_id=user.id,
        email="new-artist@magnify.music",
    )

    assert updated is not None
    assert updated.role == UserRole.ARTIST
    assert updated.artist_id == artist_id
    assert updated.email == "new-artist@magnify.music"

async def test_update_user_rejects_unknown_artist():
    repository = AsyncMock(spec=UserRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    user = User(
        email="user@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )
    repository.get_by_id.return_value = user
    artist_repository.get_by_id.return_value = None

    use_case = UpdateUser(repository, artist_repository)

    with pytest.raises(ArtistNotFoundError, match="Artist not found"):
        await use_case.execute(
            user_id=user.id,
            artist_id=uuid4(),
            artist_id_provided=True,
        )

    repository.save.assert_not_awaited()

async def test_update_user_accepts_existing_artist():
    repository = AsyncMock(spec=UserRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    user = User(
        email="user@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    artist_id = uuid4()

    repository.get_by_id.return_value = user
    artist_repository.get_by_id.return_value = Artist(
        id=artist_id,
        name="Test Artist",
    )
    repository.save.return_value = user

    use_case = UpdateUser(repository, artist_repository)

    result = await use_case.execute(
        user_id=user.id,
        artist_id=artist_id,
        artist_id_provided=True,
    )

    assert result is user
    assert user.artist_id == artist_id
    artist_repository.get_by_id.assert_awaited_once_with(artist_id)
    repository.save.assert_awaited_once()

async def test_update_artist_user_rejects_null_artist_id():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_id = uuid4()

    user = User(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )
    await repository.save(user)

    use_case = UpdateUser(repository, artist_repository)

    with pytest.raises(ValueError, match="doit être associé"):
        await use_case.execute(
            user_id=user.id,
            artist_id=None,
            artist_id_provided=True,
        )