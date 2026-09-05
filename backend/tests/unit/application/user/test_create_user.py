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