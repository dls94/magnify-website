import asyncio
from getpass import getpass

from application.exceptions import DuplicateUserEmailError
from application.use_cases.user.create_user import CreateUser
from domain.models.user import UserRole
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.artist_repository import ArtistRepository
from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.security.argon2_password_hasher import Argon2PasswordHasher


async def create_admin(
    create_user: CreateUser,
    password_hasher: Argon2PasswordHasher,
) -> None:
    email = input("Admin email: ")
    password = getpass("Admin password: ")

    password_hash = password_hasher.hash(password)

    await create_user.execute(
        email=email,
        password_hash=password_hash,
        role=UserRole.ADMIN,
    )

async def main() -> None:
    async with AsyncSessionLocal() as session:
        user_repository = UserRepository(session)
        artist_repository = ArtistRepository(session)
        password_hasher = Argon2PasswordHasher()

        create_user = CreateUser(
            repository=user_repository,
            artist_repository=artist_repository,
        )

        try:
            await create_admin(create_user, password_hasher)
        except DuplicateUserEmailError:
            print("Un utilisateur existe déjà avec cet email.")


if __name__ == "__main__":
    asyncio.run(main())