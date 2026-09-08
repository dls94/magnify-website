from infrastructure.database.dependencies import get_token_provider
from infrastructure.security.jwt_token_provider import JwtTokenProvider


def test_get_token_provider_uses_settings(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-that-is-long-enough-for-hs256",
    )
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    provider = get_token_provider()

    assert isinstance(provider, JwtTokenProvider)