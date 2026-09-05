from uuid import UUID

from application.ports.user_repository import UserRepositoryPort
from domain.models.user import User, UserRole


class UpdateUser:
    def __init__(self, repository: UserRepositoryPort) -> None:
        self.repository = repository

    async def execute(
        self,
        user_id: UUID,
        email: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> User | None:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            return None

        if email is not None:
            if not email.strip():
                raise ValueError("L'email est obligatoire.")
            if "@" not in email:
                raise ValueError("L'email est invalide.")
            user.email = email

        if role is not None:
            user.role = role

        if is_active is not None:
            if is_active and not user.is_active:
                user.activate()
            elif not is_active and user.is_active:
                user.deactivate()

        return await self.repository.save(user)