from uuid import UUID

from pydantic import BaseModel


class ArtistResponse(BaseModel):
    id: UUID
    name: str
    bio: str | None
    spotify_url: str | None
    instagram_url: str | None
    picture_url: str | None