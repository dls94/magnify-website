from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from application.ports.artist_repository import ArtistRepositoryPort
from domain.models.artist import Artist
from infrastructure.database.models.artist import ArtistModel


class ArtistRepository(ArtistRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, artist: Artist) -> Artist:
        result = await self.session.execute(
            select(ArtistModel).where(ArtistModel.id == artist.id)
        )

        artist_model = result.scalar_one_or_none()

        if artist_model is None:
            artist_model = ArtistModel(
                id=artist.id,
                name=artist.name,
                bio=artist.bio,
                spotify_url=artist.spotify_url,
                instagram_url=artist.instagram_url,
                picture_url=artist.picture_url,
                created_at=artist.created_at,
            )

            self.session.add(artist_model)
        else:
            artist_model.name = artist.name
            artist_model.bio = artist.bio
            artist_model.spotify_url = artist.spotify_url
            artist_model.instagram_url = artist.instagram_url
            artist_model.picture_url = artist.picture_url

        await self.session.commit()

        return artist

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        result = await self.session.execute(
            select(ArtistModel).where(ArtistModel.id == artist_id)
        )

        artist_model = result.scalar_one_or_none()

        if artist_model is None:
            return None

        return Artist(
            id=artist_model.id,
            name=artist_model.name,
            bio=artist_model.bio,
            spotify_url=artist_model.spotify_url,
            instagram_url=artist_model.instagram_url,
            picture_url=artist_model.picture_url,
            created_at=artist_model.created_at,
        )

    async def list_all(self) -> list[Artist]:
        result = await self.session.execute(
            select(ArtistModel)
        )

        artist_models = result.scalars().all()

        return [
            Artist(
                id=artist_model.id,
                name=artist_model.name,
                bio=artist_model.bio,
                spotify_url=artist_model.spotify_url,
                instagram_url=artist_model.instagram_url,
                picture_url=artist_model.picture_url,
                created_at=artist_model.created_at,
            )
            for artist_model in artist_models
        ]

    async def delete(self, artist_id: UUID) -> bool:
        result = await self.session.execute(
            select(ArtistModel).where(ArtistModel.id == artist_id)
        )
        artist_model = result.scalar_one_or_none()

        if artist_model is None:
            return False

        await self.session.delete(artist_model)
        await self.session.commit()

        return True