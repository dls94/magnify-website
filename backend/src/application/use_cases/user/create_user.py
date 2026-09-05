from application.ports.user_repository import UserRepositoryPort
from domain.models.user import User, UserRole


class CreateUser:
    def __init__(self, repository: UserRepositoryPort) -> None:
        self.repository = repository

    async def execute(
        self,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.ADMIN,
    ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
        )
        return await self.repository.save(user)