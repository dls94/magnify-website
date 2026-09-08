import pytest

from infrastructure.config import Settings


def test_settings_requires_jwt_secret_key(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    with pytest.raises(ValueError, match="JWT_SECRET_KEY"):
        Settings()

def test_settings_reads_jwt_configuration_from_environment(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-that-is-long-enough-for-hs256",
    )
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    settings = Settings()

    assert settings.jwt_secret_key == (
        "test-secret-key-that-is-long-enough-for-hs256"
    )
    assert settings.access_token_expire_minutes == 30