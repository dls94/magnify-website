from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure.database.models.release import ReleaseModel


class ReleaseTrackModel(Base):
    __tablename__ = "release_tracks"

    release_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("releases.id", ondelete="CASCADE"),
        primary_key=True,
    )

    track_number: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    isrc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    release: Mapped["ReleaseModel"] = relationship(
        back_populates="tracks",
    )