from application.ports.password_hasher import PasswordHasherPort
from application.ports.user_repository import UserRepositoryPort
from domain.models.user import User


class AuthenticateUser:
    def __init__(
        self,
        repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort,
    ):
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user = await self.repository.get_by_email(email)

        if user is None or not user.is_active:
            return None

        if not self.password_hasher.verify(password, user.password_hash):
            return None

        return user