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

def test_user_can_have_artist_role():
    artist_id = uuid4()

    user = User(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )

    assert user.role == UserRole.ARTIST
    assert user.artist_id == artist_id

def test_artist_user_requires_artist_id():
    with pytest.raises(
            ValueError,
            match="ARTIST doit être associé à un artiste",
    ):
        User(
            email="artist@magnify.music",
            password_hash="hashed-password",
            role=UserRole.ARTIST,
        )

def test_admin_user_does_not_require_artist_id():
    user = User(
        email="admin@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ADMIN,
    )

    assert user.artist_id is None

def test_artist_user_can_be_linked_to_artist():
    artist_id = uuid4()

    user = User(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )

    assert user.artist_id == artist_id