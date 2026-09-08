from uuid import UUID

from application.ports.token_provider import TokenProviderPort
from application.ports.user_repository import UserRepositoryPort
from domain.models.user import User


async def get_current_user(
    token: str,
    token_provider: TokenProviderPort,
    repository: UserRepositoryPort,
) -> User | None:
    payload = token_provider.decode_access_token(token)

    if payload is None:
        return None

    subject = payload.get("sub")

    if not isinstance(subject, str):
        return None

    try:
        user_id = UUID(subject)
    except ValueError:
        return None

    user = await repository.get_by_id(user_id)

    if user is None or not user.is_active:
        return None

    return user