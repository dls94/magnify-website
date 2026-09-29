import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY")

        if not self.jwt_secret_key:
            raise ValueError("JWT_SECRET_KEY est obligatoire.")

        expiration = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

        if not expiration:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES est obligatoire.")

        try:
            self.access_token_expire_minutes = int(expiration)
        except ValueError as exc:
            raise ValueError(
                "ACCESS_TOKEN_EXPIRE_MINUTES doit être un entier."
            ) from exc

        if self.access_token_expire_minutes <= 0:
            raise ValueError(
                "ACCESS_TOKEN_EXPIRE_MINUTES doit être positif."
            )