from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.ports.release_repository import ReleaseRepositoryPort
from domain.models.release import Release, ReleaseType, Track
from infrastructure.database.models.release import ReleaseModel
from infrastructure.database.models.release_track import ReleaseTrackModel


class ReleaseRepository(ReleaseRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, release: Release) -> Release:
        release_model = await self._get_model(
            release.id,
            with_tracks=True,
        )

        if release_model is None:
            release_model = ReleaseModel(
                id=release.id,
                artist_id=release.artist_id,
                title=release.title,
                release_type=release.release_type.value,
                release_date=release.release_date,
                cover_url=release.cover_url,
                upc=release.upc,
                spotify_url=release.spotify_url,
                is_published=release.is_published,
                created_at=release.created_at,
            )
            self.session.add(release_model)
        else:
            release_model.artist_id = release.artist_id
            release_model.title = release.title
            release_model.release_type = release.release_type.value
            release_model.release_date = release.release_date
            release_model.cover_url = release.cover_url
            release_model.upc = release.upc
            release_model.spotify_url = release.spotify_url
            release_model.is_published = release.is_published

            release_model.tracks.clear()

        for track in release.tracks:
            release_model.tracks.append(
                ReleaseTrackModel(
                    release_id=release.id,
                    track_number=track.track_number,
                    title=track.title,
                    duration_seconds=track.duration_seconds,
                    isrc=track.isrc,
                )
            )

        await self.session.commit()

        return release

    async def get_by_id(self, release_id: UUID) -> Release | None:
        release_model = await self._get_model(release_id, with_tracks=True)

        if release_model is None:
            return None

        release = Release(
            id=release_model.id,
            title=release_model.title,
            artist_id=release_model.artist_id,
            release_type=ReleaseType(release_model.release_type),
            release_date=release_model.release_date,
            cover_url=release_model.cover_url,
            upc=release_model.upc,
            spotify_url=release_model.spotify_url,
            is_published=release_model.is_published,
            created_at=release_model.created_at,
        )

        for track_model in release_model.tracks:
            release.tracks.append(
                Track(
                    title=track_model.title,
                    duration_seconds=track_model.duration_seconds,
                    isrc=track_model.isrc,
                    track_number=track_model.track_number,
                )
            )

        return release

    async def list_all(self) -> list[Release]:
        result = await self.session.execute(
            select(ReleaseModel).options(
                selectinload(ReleaseModel.tracks)
            )
        )
        release_models = result.scalars().all()

        return [
            self._to_domain(release_model)
            for release_model in release_models
        ]

    async def delete(self, release_id: UUID) -> bool:
        release_model = await self._get_model(release_id)

        if release_model is None:
            return False

        await self.session.delete(release_model)
        await self.session.commit()

        return True

    async def _get_model(
            self,
            release_id: UUID,
            *,
            with_tracks: bool = False,
    ) -> ReleaseModel | None:
        query = select(ReleaseModel).where(ReleaseModel.id == release_id)

        if with_tracks:
            query = query.options(selectinload(ReleaseModel.tracks))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    def _to_domain(self, release_model: ReleaseModel) -> Release:
        release = Release(
            id=release_model.id,
            title=release_model.title,
            artist_id=release_model.artist_id,
            release_type=ReleaseType(release_model.release_type),
            release_date=release_model.release_date,
            cover_url=release_model.cover_url,
            upc=release_model.upc,
            spotify_url=release_model.spotify_url,
            is_published=release_model.is_published,
            created_at=release_model.created_at,
        )

        release.tracks = [
            Track(
                title=track.title,
                duration_seconds=track.duration_seconds,
                isrc=track.isrc,
                track_number=track.track_number,
            )
            for track in release_model.tracks
        ]

        return release