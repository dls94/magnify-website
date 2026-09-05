from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from application.use_cases.event.create_event import CreateEvent
from application.use_cases.event.delete_event import DeleteEvent
from application.use_cases.event.get_event import GetEvent
from application.use_cases.event.list_events import ListEvents
from application.use_cases.event.update_event import UpdateEvent
from infrastructure.database.dependencies import (
    get_create_event_use_case,
    get_delete_event_use_case,
    get_event_use_case,
    get_list_events_use_case,
    get_update_event_use_case,
)
from interfaces.schemas.events import EventCreate, EventResponse, EventUpdate

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    data: EventCreate,
    use_case: CreateEvent = Depends(get_create_event_use_case),
) -> EventResponse:
    try:
        event = await use_case.execute(
            title=data.title,
            description=data.description,
            event_type=data.event_type,
            event_date=data.event_date,
            artist_id=data.artist_id,
            venue_name=data.venue_name,
            city=data.city,
            ticket_url=data.ticket_url,
            cover_image_url=data.cover_image_url,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return EventResponse(
        id=event.id,
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        event_date=event.event_date,
        artist_id=event.artist_id,
        venue_name=event.venue_name,
        city=event.city,
        ticket_url=event.ticket_url,
        cover_image_url=event.cover_image_url,
        is_published=event.is_published,
    )


@router.get("", response_model=list[EventResponse])
async def list_events(
    use_case: ListEvents = Depends(get_list_events_use_case),
) -> list[EventResponse]:
    events = await use_case.execute()
    return [_to_response(event) for event in events]


@router.get("/upcoming", response_model=list[EventResponse])
async def list_upcoming_events(
    use_case: ListEvents = Depends(get_list_events_use_case),
) -> list[EventResponse]:
    events = await use_case.execute_upcoming()
    return [_to_response(event) for event in events]


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: UUID,
    use_case: GetEvent = Depends(get_event_use_case),
) -> EventResponse:
    event = await use_case.execute(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return _to_response(event)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    data: EventUpdate,
    use_case: UpdateEvent = Depends(get_update_event_use_case),
) -> EventResponse:
    try:
        event = await use_case.execute(
            event_id=event_id,
            title=data.title,
            description=data.description,
            event_type=data.event_type,
            event_date=data.event_date,
            artist_id=data.artist_id,
            venue_name=data.venue_name,
            city=data.city,
            ticket_url=data.ticket_url,
            cover_image_url=data.cover_image_url,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return _to_response(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: UUID,
    use_case: DeleteEvent = Depends(get_delete_event_use_case),
) -> Response:
    deleted = await use_case.execute(event_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _to_response(event) -> EventResponse:
    return EventResponse(
        id=event.id,
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        event_date=event.event_date,
        artist_id=event.artist_id,
        venue_name=event.venue_name,
        city=event.city,
        ticket_url=event.ticket_url,
        cover_image_url=event.cover_image_url,
        is_published=event.is_published,
    )