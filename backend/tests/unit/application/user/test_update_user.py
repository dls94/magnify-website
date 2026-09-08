from uuid import uuid4

import pytest

from application.use_cases.user.update_user import UpdateUser
from domain.models.user import User, UserRole
from tests.fakes.user_repository import InMemoryUserRepository


async def test_update_user():
    repository = InMemoryUserRepository()

    user = User(
        email="admin@magnify.music",
        password_hash="hash",
    )
    await repository.save(user)

    use_case = UpdateUser(repository)

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
    use_case = UpdateUser(repository)

    result = await use_case.execute(
        uuid4(),
        email="admin@magnify.music",
    )

    assert result is None


async def test_update_user_rejects_blank_email():
    repository = InMemoryUserRepository()

    user = User(
        email="admin@magnify.music",
        password_hash="hash",
    )
    await repository.save(user)

    use_case = UpdateUser(repository)

    import pytest

    with pytest.raises(ValueError, match="L'email est obligatoire"):
        await use_case.execute(user.id, email="   ")

async def test_update_user_to_artist_requires_artist_id():
    repository = InMemoryUserRepository()
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )
    await repository.save(user)

    use_case = UpdateUser(repository)

    with pytest.raises(ValueError, match="doit être associé"):
        await use_case.execute(
            user_id=user.id,
            role=UserRole.ARTIST,
        )

async def test_update_user_to_artist_with_artist_id():
    repository = InMemoryUserRepository()
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )
    await repository.save(user)

    artist_id = uuid4()
    use_case = UpdateUser(repository)

    updated = await use_case.execute(
        user_id=user.id,
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )

    assert updated is not None
    assert updated.role == UserRole.ARTIST
    assert updated.artist_id == artist_id

async def test_update_artist_user_to_admin_clears_artist_id():
    repository = InMemoryUserRepository()
    artist_id = uuid4()

    user = User(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )
    await repository.save(user)

    use_case = UpdateUser(repository)

    updated = await use_case.execute(
        user_id=user.id,
        role=UserRole.ADMIN,
    )

    assert updated is not None
    assert updated.role == UserRole.ADMIN
    assert updated.artist_id is None

async def test_update_artist_user_without_artist_id_keeps_existing_artist_id():
    repository = InMemoryUserRepository()
    artist_id = uuid4()

    user = User(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )
    await repository.save(user)

    use_case = UpdateUser(repository)

    updated = await use_case.execute(
        user_id=user.id,
        email="new-artist@magnify.music",
    )

    assert updated is not None
    assert updated.role == UserRole.ARTIST
    assert updated.artist_id == artist_id
    assert updated.email == "new-artist@magnify.music"