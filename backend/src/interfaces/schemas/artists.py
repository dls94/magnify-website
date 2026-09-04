from uuid import UUID

from pydantic import BaseModel


class ArtistResponse(BaseModel):
    id: UUID
    name: str
    bio: str | None
    spotify_url: str | None
    instagram_url: str | None
    picture_url: str | None

class ArtistCreate(BaseModel):
    name: str
    bio: str | None = None
    spotify_url: str | None = None
    instagram_url: str | None = None
    picture_url: str | None = None

class ArtistUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None
    spotify_url: str | None = None
    instagram_url: str | None = None
    picture_url: str | None = None