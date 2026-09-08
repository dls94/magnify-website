from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user import User, UserRole
from infrastructure.database.models.user import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            artist_id=user.artist_id,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
        )

        await self.session.merge(model)
        await self.session.commit()

        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def list_all(self) -> list[User]:
        result = await self.session.execute(
            select(UserModel).order_by(UserModel.created_at)
        )
        models = result.scalars().all()

        return [self._to_domain(model) for model in models]

    async def delete(self, user_id: UUID) -> bool:
        result = await self.session.execute(
            delete(UserModel).where(UserModel.id == user_id)
        )
        await self.session.commit()

        return result.rowcount > 0

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            artist_id=model.artist_id,
            email=model.email,
            password_hash=model.password_hash,
            role=UserRole(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
        )