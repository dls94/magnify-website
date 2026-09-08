from uuid import uuid4

from application.use_cases.user.authenticate_user import AuthenticateUser
from domain.models.user import User, UserRole
from tests.fakes.user_repository import InMemoryUserRepository


class FakePasswordHasher:
    def __init__(self, valid_password: str = "correct-password"):
        self.valid_password = valid_password

    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password == self.valid_password and password_hash == "hashed:correct-password"


async def test_authenticate_user_returns_user_with_valid_credentials():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed:correct-password",
        role=UserRole.ADMIN,
    )

    repository = InMemoryUserRepository()
    await repository.save(user)

    hasher = FakePasswordHasher()
    use_case = AuthenticateUser(repository, hasher)

    result = await use_case.execute(
        email="admin@magnify.music",
        password="correct-password",
    )

    assert result == user


async def test_authenticate_user_returns_none_for_unknown_email():
    repository = InMemoryUserRepository()
    hasher = FakePasswordHasher()
    use_case = AuthenticateUser(repository, hasher)

    result = await use_case.execute(
        email="unknown@magnify.music",
        password="correct-password",
    )

    assert result is None


async def test_authenticate_user_returns_none_for_invalid_password():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed:correct-password",
        role=UserRole.ADMIN,
    )

    repository = InMemoryUserRepository()
    await repository.save(user)

    hasher = FakePasswordHasher()
    use_case = AuthenticateUser(repository, hasher)

    result = await use_case.execute(
        email="admin@magnify.music",
        password="wrong-password",
    )

    assert result is None


async def test_authenticate_user_returns_none_for_inactive_user():
    user = User(
        id=uuid4(),
        email="admin@magnify.music",
        password_hash="hashed:correct-password",
        role=UserRole.ADMIN,
    )
    user.deactivate()

    repository = InMemoryUserRepository()
    await repository.save(user)

    hasher = FakePasswordHasher()
    use_case = AuthenticateUser(repository, hasher)

    result = await use_case.execute(
        email="admin@magnify.music",
        password="correct-password",
    )

    assert result is None