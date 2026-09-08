from uuid import uuid4

from sqlalchemy import select

from domain.models.artist import Artist
from domain.models.user import User, UserRole
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.models.user import UserModel
from infrastructure.database.repositories.artist_repository import ArtistRepository
from infrastructure.database.repositories.user_repository import UserRepository


async def test_save_user_persists_user_in_database():
    user = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        saved_user = await repository.save(user)

    assert saved_user == user

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one()

    assert user_model.id == user.id
    assert user_model.email == user.email
    assert user_model.password_hash == "hashed-password"
    assert user_model.role == "ADMIN"
    assert user_model.is_active is True


async def test_get_by_id_returns_existing_user():
    user = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hashed-password",
    )

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        await repository.save(user)

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        result = await repository.get_by_id(user.id)

    assert result == user


async def test_get_by_id_returns_none_when_user_does_not_exist():
    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        result = await repository.get_by_id(uuid4())

    assert result is None


async def test_get_by_email_returns_existing_user():
    user = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hashed-password",
    )

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        await repository.save(user)

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        result = await repository.get_by_email(user.email)

    assert result == user


async def test_list_all_returns_all_users():
    user_one = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hash-one",
        role=UserRole.ADMIN,
    )
    user_two = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hash-two",
        role=UserRole.ADMIN,
    )

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        await repository.save(user_one)
        await repository.save(user_two)

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        result = await repository.list_all()

    assert user_one in result
    assert user_two in result


async def test_save_existing_user_updates_user():
    user = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="original-hash",
    )

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        await repository.save(user)

    user.email = f"updated-{uuid4()}@magnify.music"
    user.password_hash = "updated-hash"

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        await repository.save(user)

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        result = await repository.get_by_id(user.id)

    assert result is not None
    assert result.email == user.email
    assert result.password_hash == "updated-hash"


async def test_delete_removes_user():
    user = User(
        email=f"admin-{uuid4()}@magnify.music",
        password_hash="hashed-password",
    )

    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        await repository.save(user)

        deleted = await repository.delete(user.id)

        assert deleted is True

        result = await repository.get_by_id(user.id)

        assert result is None


async def test_delete_returns_false_when_user_does_not_exist():
    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)

        deleted = await repository.delete(uuid4())

    assert deleted is False

async def test_save_and_get_artist_user_with_artist_id():
    artist = Artist(
        name=f"Test Artist {uuid4()}",
    )

    async with AsyncSessionLocal() as session:
        artist_repository = ArtistRepository(session)
        await artist_repository.save(artist)

    user = User(
        email=f"artist-{uuid4()}@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist.id,
    )

    async with AsyncSessionLocal() as session:
        user_repository = UserRepository(session)

        await user_repository.save(user)

    async with AsyncSessionLocal() as session:
        user_repository = UserRepository(session)

        result = await user_repository.get_by_id(user.id)

    assert result is not None
    assert result.id == user.id
    assert result.role == UserRole.ARTIST
    assert result.artist_id == artist.id