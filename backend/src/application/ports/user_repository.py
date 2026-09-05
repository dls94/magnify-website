from typing import Protocol
from uuid import UUID

from domain.models.user import User


class UserRepositoryPort(Protocol):
    async def save(self, user: User) -> User:
        ...

    async def get_by_id(self, user_id: UUID) -> User | None:
        ...

    async def get_by_email(self, email: str) -> User | None:
        ...

    async def list_all(self) -> list[User]:
        ...

    async def delete(self, user_id: UUID) -> bool:
        ...