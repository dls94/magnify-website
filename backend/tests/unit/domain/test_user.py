from datetime import UTC, datetime
from uuid import uuid4

import pytest

from domain.models.user import User, UserRole


def test_create_user():
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
    )

    assert user.email == "admin@magnify.music"
    assert user.password_hash == "hashed-password"
    assert user.role == UserRole.ADMIN
    assert user.is_active is True
    assert user.id is not None
    assert user.created_at.tzinfo == UTC


def test_create_user_with_custom_id_and_date():
    user_id = uuid4()
    created_at = datetime(2026, 9, 5, 18, 0, tzinfo=UTC)

    user = User(
        id=user_id,
        email="admin@magnify.music",
        password_hash="hashed-password",
        created_at=created_at,
    )

    assert user.id == user_id
    assert user.created_at == created_at


def test_create_user_rejects_blank_email():
    with pytest.raises(ValueError, match="L'email est obligatoire"):
        User(
            email="   ",
            password_hash="hashed-password",
        )


def test_create_user_rejects_invalid_email():
    with pytest.raises(ValueError, match="L'email est invalide"):
        User(
            email="admin",
            password_hash="hashed-password",
        )


def test_create_user_rejects_empty_password_hash():
    with pytest.raises(
        ValueError,
        match="Le mot de passe hashé est obligatoire",
    ):
        User(
            email="admin@magnify.music",
            password_hash="",
        )


def test_deactivate_user():
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
    )

    user.deactivate()

    assert user.is_active is False


def test_deactivate_user_twice_fails():
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
    )

    user.deactivate()

    with pytest.raises(ValueError, match="déjà désactivé"):
        user.deactivate()


def test_activate_user():
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
    )

    user.deactivate()
    user.activate()

    assert user.is_active is True


def test_activate_active_user_fails():
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
    )

    with pytest.raises(ValueError, match="déjà actif"):
        user.activate()