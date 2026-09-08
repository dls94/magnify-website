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
        artist_id: UUID | None = None,
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

        target_role = role if role is not None else user.role

        if target_role == UserRole.ARTIST:
            if artist_id is not None:
                user.artist_id = artist_id
            elif user.artist_id is None:
                raise ValueError("Un utilisateur ARTIST doit être associé à un artiste.")

        elif target_role == UserRole.ADMIN and role == UserRole.ADMIN:
                user.artist_id = artist_id

        user.role = target_role

        if is_active is not None:
            if is_active and not user.is_active:
                user.activate()
            elif not is_active and user.is_active:
                user.deactivate()

        return await self.repository.save(user)