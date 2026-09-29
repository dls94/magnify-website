from uuid import UUID

from pydantic import BaseModel

from magnify_core.domain.models import UserRole


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthenticatedUserResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: AuthenticatedUserResponse