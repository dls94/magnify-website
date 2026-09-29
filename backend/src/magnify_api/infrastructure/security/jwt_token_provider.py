from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt import InvalidTokenError


class JwtTokenProvider:
    ALGORITHM = "HS256"

    def __init__(
        self,
        secret_key: str,
        access_token_expire_minutes: int,
    ) -> None:
        if not secret_key:
            raise ValueError("La clé secrète JWT est obligatoire.")

        if access_token_expire_minutes <= 0:
            raise ValueError(
                "La durée de validité du token doit être positive."
            )

        self._secret_key = secret_key
        self._access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(
        self,
        subject: str,
        claims: dict[str, Any],
    ) -> str:
        now = datetime.now(UTC)
        expires_at = now + timedelta(
            minutes=self._access_token_expire_minutes
        )

        payload = {
            "sub": subject,
            "iat": now,
            "exp": expires_at,
            **claims,
        }

        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self.ALGORITHM,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, Any] | None:
        try:
            return jwt.decode(
                token,
                self._secret_key,
                algorithms=[self.ALGORITHM],
            )
        except InvalidTokenError:
            return None