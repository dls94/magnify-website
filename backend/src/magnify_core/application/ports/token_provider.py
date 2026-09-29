from typing import Any, Protocol


class TokenProviderPort(Protocol):
    def create_access_token(
        self,
        subject: str,
        claims: dict[str, Any],
    ) -> str:
        ...

    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, Any] | None:
        ...