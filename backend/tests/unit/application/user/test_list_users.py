from application.use_cases.user.list_users import ListUsers
from domain.models.user import User
from tests.fakes.user_repository import InMemoryUserRepository


async def test_list_users():
    repository = InMemoryUserRepository()

    first_user = User(
        email="first@magnify.music",
        password_hash="hash",
    )
    second_user = User(
        email="second@magnify.music",
        password_hash="hash",
    )

    await repository.save(first_user)
    await repository.save(second_user)

    use_case = ListUsers(repository)

    users = await use_case.execute()

    assert users == [first_user, second_user]