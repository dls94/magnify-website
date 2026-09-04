from fastapi import APIRouter, Depends

from application.use_cases.artist.list_artists import ListArtists
from infrastructure.database.dependencies import get_list_artists_use_case
from interfaces.schemas.artists import ArtistResponse

router = APIRouter(
    prefix="/api/v1/artists",
    tags=["artists"],
)


@router.get("")
async def list_artists(
    use_case: ListArtists = Depends(get_list_artists_use_case),
) -> list[ArtistResponse]:
    return await use_case.execute()