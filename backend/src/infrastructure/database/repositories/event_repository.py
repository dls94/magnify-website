from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.event_repository import EventRepositoryPort
from domain.models.event import Event, EventType
from infrastructure.database.models.event import EventModel


class EventRepository(EventRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, event: Event) -> Event:
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event.id)
        )
        event_model = result.scalar_one_or_none()

        if event_model is None:
            event_model = EventModel(
                id=event.id,
                artist_id=event.artist_id,
                title=event.title,
                description=event.description,
                event_type=event.event_type.value,
                event_date=event.event_date,
                venue_name=event.venue_name,
                city=event.city,
                ticket_url=event.ticket_url,
                cover_image_url=event.cover_image_url,
                is_published=event.is_published,
                created_at=event.created_at,
            )
            self.session.add(event_model)
        else:
            event_model.artist_id = event.artist_id
            event_model.title = event.title
            event_model.description = event.description
            event_model.event_type = event.event_type.value
            event_model.event_date = event.event_date
            event_model.venue_name = event.venue_name
            event_model.city = event.city
            event_model.ticket_url = event.ticket_url
            event_model.cover_image_url = event.cover_image_url
            event_model.is_published = event.is_published

        await self.session.commit()

        return event

    async def get_by_id(self, event_id: UUID) -> Event | None:
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )
        event_model = result.scalar_one_or_none()

        if event_model is None:
            return None

        return self._to_domain(event_model)

    async def list_all(self) -> list[Event]:
        result = await self.session.execute(
            select(EventModel).order_by(EventModel.event_date)
        )
        event_models = result.scalars().all()

        return [self._to_domain(event_model) for event_model in event_models]

    async def list_upcoming(self) -> list[Event]:
        now = datetime.now(UTC)

        result = await self.session.execute(
            select(EventModel)
            .where(EventModel.event_date >= now)
            .order_by(EventModel.event_date)
        )
        event_models = result.scalars().all()

        return [self._to_domain(event_model) for event_model in event_models]

    async def delete(self, event_id: UUID) -> bool:
        result = await self.session.execute(
            delete(EventModel).where(EventModel.id == event_id)
        )

        if result.rowcount == 0:
            return False

        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(event_model: EventModel) -> Event:
        return Event(
            id=event_model.id,
            artist_id=event_model.artist_id,
            title=event_model.title,
            description=event_model.description,
            event_type=EventType(event_model.event_type),
            event_date=event_model.event_date,
            venue_name=event_model.venue_name,
            city=event_model.city,
            ticket_url=event_model.ticket_url,
            cover_image_url=event_model.cover_image_url,
            is_published=event_model.is_published,
            created_at=event_model.created_at,
        )