from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from domain.models.release import ReleaseType


class ReleaseCreate(BaseModel):
    title: str = Field(min_length=1)
    artist_id: UUID | None = None
    release_type: ReleaseType
    release_date: date
    cover_url: HttpUrl | None = None


class ReleaseResponse(BaseModel):
    id: UUID
    title: str
    artist_id: UUID | None
    release_type: ReleaseType
    release_date: date
    cover_url: str | None = None


class ReleaseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    artist_id: UUID | None = None
    release_type: ReleaseType | None = None
    release_date: date | None = None
    cover_url: HttpUrl | None = None
    upc: str | None = None
    spotify_url: HttpUrl | None = None