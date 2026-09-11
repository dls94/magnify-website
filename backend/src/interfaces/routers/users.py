from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from application.exceptions import (
    ArtistNotFoundError,
    DuplicateUserEmailError,
)
from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.delete_user import DeleteUser
from application.use_cases.user.get_user import GetUser
from application.use_cases.user.list_users import ListUsers
from application.use_cases.user.update_user import UpdateUser
from domain.models.user import User
from infrastructure.database.dependencies import (
    get_create_user_use_case,
    get_delete_user_use_case,
    get_get_user_use_case,
    get_list_users_use_case,
    get_password_hasher,
    get_update_user_use_case,
)
from infrastructure.security.admin_access import require_admin
from infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from interfaces.schemas.users import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    use_case: CreateUser = Depends(get_create_user_use_case),
    password_hasher: Argon2PasswordHasher = Depends(get_password_hasher),
    _: User = Depends(require_admin),
) -> UserResponse:
    try:
        user = await use_case.execute(
            email=data.email,
            password_hash=password_hasher.hash(data.password),
            role=data.role,
            artist_id=data.artist_id,
        )
    except ArtistNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except DuplicateUserEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un utilisateur avec cet email existe déjà.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        artist_id=user.artist_id,
        is_active=user.is_active,
    )

@router.get("", response_model=list[UserResponse])
async def list_users(
    use_case: ListUsers = Depends(get_list_users_use_case),
    _: User = Depends(require_admin),
) -> list[UserResponse]:
    users = await use_case.execute()

    return [
        UserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            artist_id=user.artist_id,
            is_active=user.is_active,
        )
        for user in users
    ]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    use_case: GetUser = Depends(get_get_user_use_case),
    _: User = Depends(require_admin),
) -> UserResponse:
    user = await use_case.execute(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable.",
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        artist_id=user.artist_id,
        is_active=user.is_active,
    )

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    use_case: UpdateUser = Depends(get_update_user_use_case),
    _: User = Depends(require_admin),
) -> UserResponse:
    try:
        user = await use_case.execute(
            user_id=user_id,
            email=data.email,
            role=data.role,
            artist_id=data.artist_id,
            artist_id_provided="artist_id" in data.model_fields_set,
            is_active=data.is_active,
        )
    except DuplicateUserEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un utilisateur avec cet email existe déjà.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except ArtistNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable.",
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        artist_id=user.artist_id,
        is_active=user.is_active,
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    use_case: DeleteUser = Depends(get_delete_user_use_case),
    _: User = Depends(require_admin),
) -> Response:
    deleted = await use_case.execute(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

