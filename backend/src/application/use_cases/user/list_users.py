from application.ports.user_repository import UserRepositoryPort
from domain.models.user import User


class ListUsers:
    def __init__(self, repository: UserRepositoryPort) -> None:
        self.repository = repository

    async def execute(self) -> list[User]:
        return await self.repository.list_all()