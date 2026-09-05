from uuid import UUID

from application.ports.user_repository import UserRepositoryPort


class DeleteUser:
    def __init__(self, repository: UserRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, user_id: UUID) -> bool:
        return await self.repository.delete(user_id)