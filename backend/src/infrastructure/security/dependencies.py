from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from application.ports.token_provider import TokenProviderPort
from application.ports.user_repository import UserRepositoryPort
from domain.models.user import User
from infrastructure.database.dependencies import (
    get_token_provider,
    get_user_repository,
)
from infrastructure.security.current_user import (
    get_current_user as resolve_current_user,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


async def get_authenticated_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_provider: TokenProviderPort = Depends(get_token_provider),
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> User:
    user = await resolve_current_user(
        token=token,
        token_provider=token_provider,
        repository=repository,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou utilisateur non authentifié.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user