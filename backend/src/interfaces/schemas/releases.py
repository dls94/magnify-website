from datetime import date
from uuid import UUID

from pydantic import BaseModel

from domain.models.release import ReleaseType


class ReleaseCreate(BaseModel):
    title: str
    artist_id: UUID | None = None
    release_type: ReleaseType
    release_date: date
    cover_url: str | None = None


class ReleaseResponse(BaseModel):
    id: UUID
    title: str
    artist_id: UUID | None
    release_type: ReleaseType
    release_date: date
    cover_url: str | None


class ReleaseUpdate(BaseModel):
    title: str | None = None
    artist_id: UUID | None = None
    release_type: ReleaseType | None = None
    release_date: date | None = None
    cover_url: str | None = None
    upc: str | None = None
    spotify_url: str | None = None