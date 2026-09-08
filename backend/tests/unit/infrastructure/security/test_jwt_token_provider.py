from datetime import UTC, datetime, timedelta

import jwt

from infrastructure.security.jwt_token_provider import JwtTokenProvider


def test_create_access_token_returns_token():
    provider = JwtTokenProvider(
        secret_key="test-secret-key-that-is-long-enough-for-hs256",
        access_token_expire_minutes=30,
    )

    token = provider.create_access_token(
        subject="user-id",
        claims={"role": "ADMIN"},
    )

    assert isinstance(token, str)
    assert token


def test_decode_access_token_returns_claims():
    provider = JwtTokenProvider(
        secret_key="test-secret-key-that-is-long-enough-for-hs256",
        access_token_expire_minutes=30,
    )

    token = provider.create_access_token(
        subject="user-id",
        claims={"role": "ADMIN"},
    )

    payload = provider.decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "user-id"
    assert payload["role"] == "ADMIN"


def test_decode_access_token_returns_none_for_invalid_token():
    provider = JwtTokenProvider(
        secret_key="test-secret-key-that-is-long-enough-for-hs256",
        access_token_expire_minutes=30,
    )

    result = provider.decode_access_token("invalid-token")

    assert result is None


def test_decode_access_token_returns_none_for_token_signed_with_wrong_key():
    provider = JwtTokenProvider(
        secret_key="test-secret-key-that-is-long-enough-for-hs256",
        access_token_expire_minutes=30,
    )
    other_provider = JwtTokenProvider(
        secret_key="other-secret-key-that-is-long-enough-for-hs256",
        access_token_expire_minutes=30,
    )

    token = other_provider.create_access_token(
        subject="user-id",
        claims={"role": "ADMIN"},
    )

    result = provider.decode_access_token(token)

    assert result is None


def test_decode_access_token_returns_none_for_expired_token():
    provider = JwtTokenProvider(
        secret_key="test-secret-key-that-is-long-enough-for-hs256",
        access_token_expire_minutes=30,
    )

    expired_token = jwt.encode(
        {
            "sub": "user-id",
            "role": "ADMIN",
            "iat": datetime.now(UTC) - timedelta(minutes=2),
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        "test-secret-key-that-is-long-enough-for-hs256",
        algorithm=JwtTokenProvider.ALGORITHM,
    )

    result = provider.decode_access_token(expired_token)

    assert result is None