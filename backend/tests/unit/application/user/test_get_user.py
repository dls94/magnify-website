from application.use_cases.user.get_user import GetUser
from domain.models.user import User
from tests.fakes.user_repository import InMemoryUserRepository


async def test_get_user():
    repository = InMemoryUserRepository()
    user = User(
        email="admin@magnify.music",
        password_hash="hash",
    )
    await repository.save(user)

    use_case = GetUser(repository)

    result = await use_case.execute(user.id)

    assert result is user


async def test_get_user_returns_none_when_not_found():
    repository = InMemoryUserRepository()
    use_case = GetUser(repository)

    result = await use_case.execute(__import__("uuid").uuid4())

    assert result is None