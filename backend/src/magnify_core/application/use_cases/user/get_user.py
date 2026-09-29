from uuid import UUID

from magnify_core.application.ports.user_repository import UserRepositoryPort
from magnify_core.domain.models import User


class GetUser:
    def __init__(self, repository: UserRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, user_id: UUID) -> User | None:
        return await self.repository.get_by_id(user_id)