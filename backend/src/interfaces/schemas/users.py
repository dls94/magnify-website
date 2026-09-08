from uuid import UUID

from pydantic import BaseModel

from domain.models.user import UserRole


class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole = UserRole.ADMIN
    artist_id: UUID | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole
    artist_id: UUID | None
    is_active: bool


class UserUpdate(BaseModel):
    email: str | None = None
    role: UserRole | None = None
    artist_id: UUID | None = None
    is_active: bool | None = None