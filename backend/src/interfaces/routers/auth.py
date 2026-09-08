from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.user.authenticate_user import AuthenticateUser
from domain.models.user import User
from infrastructure.database.dependencies import (
    get_authenticate_user,
    get_token_provider,
)
from infrastructure.security.dependencies import get_authenticated_user
from infrastructure.security.jwt_token_provider import JwtTokenProvider
from interfaces.schemas.auth import (
    AuthenticatedUserResponse,
    LoginRequest,
    TokenResponse,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    authenticate_user: AuthenticateUser = Depends(get_authenticate_user),
    token_provider: JwtTokenProvider = Depends(get_token_provider),
) -> TokenResponse:
    user = await authenticate_user.execute(
        email=request.email,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
        )

    access_token = token_provider.create_access_token(
        subject=str(user.id),
        claims={"role": user.role.value},
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=AuthenticatedUserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
        ),
    )

@router.get(
    "/me",
    response_model=AuthenticatedUserResponse,
)
async def get_me(
    current_user: User = Depends(get_authenticated_user),
) -> AuthenticatedUserResponse:
    return AuthenticatedUserResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
    )