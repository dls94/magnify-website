from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.models.event import EventType


class EventCreate(BaseModel):
    title: str
    description: str
    event_type: EventType
    event_date: datetime
    artist_id: UUID | None = None
    venue_name: str | None = None
    city: str | None = None
    ticket_url: str | None = None
    cover_image_url: str | None = None


class EventResponse(BaseModel):
    id: UUID
    title: str
    description: str
    event_type: EventType
    event_date: datetime
    artist_id: UUID | None
    venue_name: str | None
    city: str | None
    ticket_url: str | None
    cover_image_url: str | None
    is_published: bool


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    event_type: EventType | None = None
    event_date: datetime | None = None
    artist_id: UUID | None = None
    venue_name: str | None = None
    city: str | None = None
    ticket_url: str | None = None
    cover_image_url: str | None = None