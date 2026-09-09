from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from domain.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
    role: UserRole = UserRole.ADMIN
    artist_id: UUID | None = None


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    artist_id: UUID | None
    is_active: bool


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: UserRole | None = None
    artist_id: UUID | None = None
    is_active: bool | None = None