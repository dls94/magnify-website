from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.artist.get_current_artist import GetCurrentArtist
from application.use_cases.release.get_current_artist_releases import (
    GetCurrentArtistReleases,
)
from domain.models.user import User
from infrastructure.database.dependencies import (
    get_current_artist_releases_use_case,
    get_current_artist_use_case,
)
from infrastructure.security.dependencies import get_authenticated_user
from interfaces.schemas.artists import ArtistResponse
from interfaces.schemas.releases import ReleaseResponse

router = APIRouter(prefix="/api/v1/me", tags=["me"])

@router.get("/artist", response_model=ArtistResponse)
async def get_current_artist(
    current_user: User = Depends(get_authenticated_user),
    use_case: GetCurrentArtist = Depends(get_current_artist_use_case),
) -> ArtistResponse:
    artist = await use_case.execute(current_user)

    if artist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artiste introuvable.",
        )

    return ArtistResponse(
        id=artist.id,
        name=artist.name,
        bio=artist.bio,
        spotify_url=artist.spotify_url,
        instagram_url=artist.instagram_url,
        picture_url=artist.picture_url,
    )

@router.get("/releases", response_model=list[ReleaseResponse])
async def get_current_artist_releases(
    current_user: User = Depends(get_authenticated_user),
    use_case: GetCurrentArtistReleases = Depends(
        get_current_artist_releases_use_case
    ),
) -> list[ReleaseResponse]:
    releases = await use_case.execute(current_user)

    return [
        ReleaseResponse(
            id=release.id,
            title=release.title,
            artist_id=release.artist_id,
            release_type=release.release_type,
            release_date=release.release_date,
            cover_url=release.cover_url,
        )
        for release in releases
    ]