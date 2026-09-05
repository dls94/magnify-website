from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from application.use_cases.artist.create_artist import CreateArtist
from application.use_cases.artist.delete_artist import DeleteArtist
from application.use_cases.artist.get_artist import GetArtist
from application.use_cases.artist.list_artists import ListArtists
from application.use_cases.artist.update_artist import UpdateArtist
from infrastructure.database.dependencies import (
    get_artist_use_case,
    get_create_artist_use_case,
    get_delete_artist_use_case,
    get_list_artists_use_case,
    get_update_artist_use_case,
)
from interfaces.schemas.artists import ArtistCreate, ArtistResponse, ArtistUpdate

router = APIRouter(
    prefix="/api/v1/artists",
    tags=["artists"],
)


@router.get("")
async def list_artists(
    use_case: ListArtists = Depends(get_list_artists_use_case),
) -> list[ArtistResponse]:
    return await use_case.execute()

@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(
    artist_id: UUID,
    use_case: GetArtist = Depends(get_artist_use_case),
) -> ArtistResponse:
    artist = await use_case.execute(artist_id)

    if artist is None:
        raise HTTPException(
            status_code=404,
            detail="Artist not found",
        )

    return artist

@router.post("", response_model=ArtistResponse, status_code=201)
async def create_artist(
    payload: ArtistCreate,
    use_case: CreateArtist = Depends(get_create_artist_use_case),
) -> ArtistResponse:
    try:
        return await use_case.execute(
            name=payload.name,
            bio=payload.bio,
            spotify_url=payload.spotify_url,
            instagram_url=payload.instagram_url,
            picture_url=payload.picture_url,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

@router.patch("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: UUID,
    payload: ArtistUpdate,
    use_case: UpdateArtist = Depends(get_update_artist_use_case),
) -> ArtistResponse:
    artist = await use_case.execute(
        artist_id=artist_id,
        name=payload.name,
        bio=payload.bio,
        picture_url=payload.picture_url,
        spotify_url=payload.spotify_url,
        instagram_url=payload.instagram_url,
    )

    if artist is None:
        raise HTTPException(
            status_code=404,
            detail="Artist not found",
        )

    return artist

@router.delete("/{artist_id}", status_code=204)
async def delete_artist(
    artist_id: UUID,
    use_case: DeleteArtist = Depends(get_delete_artist_use_case),
) -> None:
    deleted = await use_case.execute(artist_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Artist not found",
        )