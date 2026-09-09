from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class ArtistResponse(BaseModel):
    id: UUID
    name: str
    bio: str | None
    spotify_url: str | None
    instagram_url: str | None
    picture_url: str | None

class ArtistCreate(BaseModel):
    name: str = Field(min_length=1)
    bio: str | None = None
    spotify_url: HttpUrl | None = None
    instagram_url: HttpUrl | None = None
    picture_url: HttpUrl | None = None

class ArtistUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    bio: str | None = None
    spotify_url: HttpUrl | None = None
    instagram_url: HttpUrl | None = None
    picture_url: HttpUrl | None = None