from unittest.mock import AsyncMock, Mock, patch

import pytest

from domain.models.user import UserRole
from scripts.create_admin import create_admin, main


@pytest.mark.asyncio
async def test_create_admin_creates_admin_user():
    create_user = Mock()
    create_user.execute = AsyncMock()

    password_hasher = Mock()
    password_hasher.hash.return_value = "hashed-password"

    with (
        patch("scripts.create_admin.input", return_value="admin@magnify.music"),
        patch("scripts.create_admin.getpass", return_value="super-secret"),
    ):
        await create_admin(create_user, password_hasher)

    password_hasher.hash.assert_called_once_with("super-secret")

    create_user.execute.assert_awaited_once_with(
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

@pytest.mark.asyncio
async def test_main_builds_dependencies_and_runs_bootstrap():
    with (
        patch("scripts.create_admin.AsyncSessionLocal") as session_factory,
        patch("scripts.create_admin.create_admin", new_callable=AsyncMock) as bootstrap,
    ):
        await main()

    bootstrap.assert_awaited_once()
    session_factory.assert_called_once()

@pytest.mark.asyncio
async def test_create_admin_propagates_duplicate_email_error():
    from application.exceptions import DuplicateUserEmailError

    create_user = Mock()
    create_user.execute = AsyncMock(
        side_effect=DuplicateUserEmailError,
    )

    password_hasher = Mock()
    password_hasher.hash.return_value = "hashed-password"

    with (
        patch(
            "scripts.create_admin.input",
            return_value="admin@magnify.music",
        ),
        patch(
            "scripts.create_admin.getpass",
            return_value="super-secret",
        ),
        pytest.raises(DuplicateUserEmailError),
    ):
        await create_admin(create_user, password_hasher)

@pytest.mark.asyncio
async def test_main_reports_duplicate_email(capsys):
    from application.exceptions import DuplicateUserEmailError

    with (
        patch("scripts.create_admin.AsyncSessionLocal"),
        patch(
            "scripts.create_admin.create_admin",
            new_callable=AsyncMock,
            side_effect=DuplicateUserEmailError,
        ),
    ):
        await main()

    captured = capsys.readouterr()

    assert "Un utilisateur existe déjà avec cet email." in captured.out