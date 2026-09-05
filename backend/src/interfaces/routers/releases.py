from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from application.use_cases.release.create_release import CreateRelease
from application.use_cases.release.get_release import GetRelease
from application.use_cases.release.list_releases import ListReleases
from application.use_cases.release.update_release import UpdateRelease
from application.use_cases.release.delete_release import DeleteRelease
from domain.models.release import Release
from infrastructure.database.dependencies import (
    get_create_release_use_case,
    get_release_use_case,
    get_list_releases_use_case,
    get_update_release_use_case,
    get_delete_release_use_case,
)
from interfaces.schemas.releases import ReleaseCreate, ReleaseResponse, ReleaseUpdate


router = APIRouter(
    prefix="/api/v1/releases",
    tags=["releases"],
)


@router.post(
    "",
    response_model=ReleaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_release(
    data: ReleaseCreate,
    use_case: CreateRelease = Depends(get_create_release_use_case),
) -> Release:
    try:
        return await use_case.execute(
            title=data.title,
            artist_id=data.artist_id,
            release_type=data.release_type,
            release_date=data.release_date,
            cover_url=data.cover_url,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.get(
    "/{release_id}",
    response_model=ReleaseResponse,
)
async def get_release(
    release_id: UUID,
    use_case: GetRelease = Depends(get_release_use_case),
) -> Release:
    release = await use_case.execute(release_id)

    if release is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release not found",
        )

    return release

@router.get(
    "",
    response_model=list[ReleaseResponse],
)
async def list_releases(
    use_case: ListReleases = Depends(get_list_releases_use_case),
) -> list[Release]:
    return await use_case.execute()

@router.patch(
    "/{release_id}",
    response_model=ReleaseResponse,
)
async def update_release(
    release_id: UUID,
    data: ReleaseUpdate,
    use_case: UpdateRelease = Depends(get_update_release_use_case),
) -> Release:
    try:
        release = await use_case.execute(
            release_id=release_id,
            title=data.title,
            artist_id=data.artist_id,
            release_type=data.release_type,
            release_date=data.release_date,
            cover_url=data.cover_url,
            upc=data.upc,
            spotify_url=data.spotify_url,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if release is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release not found",
        )

    return release

@router.delete(
    "/{release_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_release(
    release_id: UUID,
    use_case: DeleteRelease = Depends(get_delete_release_use_case),
) -> None:
    deleted = await use_case.execute(release_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release not found",
        )