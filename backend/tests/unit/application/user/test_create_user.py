from uuid import uuid4

from application.use_cases.user.create_user import CreateUser
from domain.models.user import UserRole
from tests.fakes.user_repository import InMemoryUserRepository


async def test_create_user():
    repository = InMemoryUserRepository()
    use_case = CreateUser(repository)

    user = await use_case.execute(
        email="admin@magnify.music",
        password_hash="hashed-password",
    )

    assert user.email == "admin@magnify.music"
    assert user.password_hash == "hashed-password"
    assert user.role == UserRole.ADMIN
    assert user.id in repository.users

async def test_create_artist_user_with_artist_id():
    repository = InMemoryUserRepository()
    use_case = CreateUser(repository)

    artist_id = uuid4()

    user = await use_case.execute(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )

    assert user.email == "artist@magnify.music"
    assert user.password_hash == "hashed-password"
    assert user.role == UserRole.ARTIST
    assert user.artist_id == artist_id
    assert user.id in repository.users