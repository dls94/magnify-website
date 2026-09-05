from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure.database.models.release_track import ReleaseTrackModel


class ReleaseModel(Base):
    __tablename__ = "releases"

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

    release_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    release_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    cover_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    upc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    spotify_url: Mapped[str | None] = mapped_column(
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

    tracks: Mapped[list["ReleaseTrackModel"]] = relationship(
        back_populates="release",
        cascade="all, delete-orphan",
        order_by="ReleaseTrackModel.track_number",
    )