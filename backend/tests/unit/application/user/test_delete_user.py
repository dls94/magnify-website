from application.use_cases.user.delete_user import DeleteUser
from domain.models.user import User
from tests.fakes.user_repository import InMemoryUserRepository


async def test_delete_user():
    repository = InMemoryUserRepository()

    user = User(
        email="admin@magnify.music",
        password_hash="hash",
    )
    await repository.save(user)

    use_case = DeleteUser(repository)

    deleted = await use_case.execute(user.id)

    assert deleted is True
    assert await repository.get_by_id(user.id) is None


async def test_delete_user_returns_false_when_not_found():
    from uuid import uuid4

    repository = InMemoryUserRepository()
    use_case = DeleteUser(repository)

    deleted = await use_case.execute(uuid4())

    assert deleted is False