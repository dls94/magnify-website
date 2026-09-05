from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.artist import ArtistModel


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )

    artist_id: Mapped[UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("artists.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    venue_name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ticket_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cover_image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_published: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    if TYPE_CHECKING:
        artist: Mapped["ArtistModel | None"]

    artist = relationship("ArtistModel")