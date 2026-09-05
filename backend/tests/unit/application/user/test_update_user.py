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