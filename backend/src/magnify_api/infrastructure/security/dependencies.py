from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from magnify_api.infrastructure.database.dependencies import (
    get_token_provider,
    get_user_repository,
)
from magnify_api.infrastructure.security.current_user import (
    get_current_user as resolve_current_user,
)
from magnify_core.application.ports.token_provider import TokenProviderPort
from magnify_core.application.ports.user_repository import UserRepositoryPort
from magnify_core.domain.models import User

bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
)

async def get_authenticated_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_scheme),
    ],
    token_provider: TokenProviderPort = Depends(get_token_provider),
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> User:
    user = await resolve_current_user(
        token=credentials.credentials,
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