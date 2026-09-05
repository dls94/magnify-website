from uuid import UUID

from application.ports.user_repository import UserRepositoryPort
from domain.models.user import User


class GetUser:
    def __init__(self, repository: UserRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, user_id: UUID) -> User | None:
        return await self.repository.get_by_id(user_id)