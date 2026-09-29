from uuid import UUID

from magnify_core.application.exceptions import ArtistNotFoundError
from magnify_core.application.ports.artist_repository import ArtistRepositoryPort
from magnify_core.application.ports.user_repository import UserRepositoryPort
from magnify_core.domain.models import User, UserRole


class CreateUser:
    def __init__(
        self,
        repository: UserRepositoryPort,
        artist_repository: ArtistRepositoryPort,
    ) -> None:
        self.repository = repository
        self.artist_repository = artist_repository

    async def execute(
        self,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.ADMIN,
        artist_id: UUID | None = None,
    ) -> User:
        if artist_id is not None:
            artist = await self.artist_repository.get_by_id(artist_id)

            if artist is None:
                raise ArtistNotFoundError("Artist not found")

        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
            artist_id=artist_id,
        )

        return await self.repository.save(user)