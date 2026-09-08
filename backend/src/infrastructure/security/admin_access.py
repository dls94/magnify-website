from fastapi import Depends, HTTPException, status

from domain.models.user import User, UserRole
from infrastructure.security.dependencies import get_authenticated_user


async def require_admin(
    user: User = Depends(get_authenticated_user),
) -> User:
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis.",
        )
    return user