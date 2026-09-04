from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class ArtistModel(Base):
    __tablename__ = "artists"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    spotify_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    instagram_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    picture_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )