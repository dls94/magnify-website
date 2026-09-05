from uuid import UUID

from domain.models.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}

    async def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.users.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return next(
            (user for user in self.users.values() if user.email == email),
            None,
        )

    async def list_all(self) -> list[User]:
        return list(self.users.values())

    async def delete(self, user_id: UUID) -> bool:
        if user_id not in self.users:
            return False

        del self.users[user_id]
        return True