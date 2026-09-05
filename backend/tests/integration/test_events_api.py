from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_event():
    response = client.post(
        "/api/v1/events",
        json={
            "title": "Concert Magnify",
            "description": "Un concert Magnify Music.",
            "event_type": "CONCERT",
            "event_date": "2026-10-15T20:00:00Z",
            "venue_name": "La Cigale",
            "city": "Paris",
            "ticket_url": "https://example.com/tickets",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Concert Magnify"
    assert data["description"] == "Un concert Magnify Music."
    assert data["event_type"] == "CONCERT"
    assert data["venue_name"] == "La Cigale"
    assert data["city"] == "Paris"
    assert data["is_published"] is False
    assert "id" in data


def test_create_event_rejects_blank_title():
    response = client.post(
        "/api/v1/events",
        json={
            "title": "   ",
            "description": "Description",
            "event_type": "CONCERT",
            "event_date": "2026-10-15T20:00:00Z",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Le titre de l'événement est obligatoire."


def test_create_event_rejects_naive_datetime():
    response = client.post(
        "/api/v1/events",
        json={
            "title": "Concert Magnify",
            "description": "Description",
            "event_type": "CONCERT",
            "event_date": "2026-10-15T20:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "La date doit être timezone-aware."


def test_get_event():
    create_response = client.post(
        "/api/v1/events",
        json={
            "title": "Event à récupérer",
            "description": "Description",
            "event_type": "CONCERT",
            "event_date": "2026-10-20T20:00:00Z",
        },
    )

    event_id = create_response.json()["id"]

    response = client.get(f"/api/v1/events/{event_id}")

    assert response.status_code == 200
    assert response.json()["id"] == event_id
    assert response.json()["title"] == "Event à récupérer"


def test_get_event_returns_404_when_not_found():
    response = client.get(
        "/api/v1/events/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_list_events():
    response = client.get("/api/v1/events")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_upcoming_events():
    response = client.get("/api/v1/events/upcoming")

    assert response.status_code == 200

    events = response.json()

    assert isinstance(events, list)

    now = datetime.now(UTC)

    for event in events:
        event_date = datetime.fromisoformat(event["event_date"])
        assert event_date >= now - timedelta(seconds=5)


def test_update_event():
    create_response = client.post(
        "/api/v1/events",
        json={
            "title": "Event initial",
            "description": "Description initiale",
            "event_type": "CONCERT",
            "event_date": "2026-10-20T20:00:00Z",
        },
    )

    event_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/events/{event_id}",
        json={
            "title": "Event modifié",
            "city": "Paris",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == event_id
    assert data["title"] == "Event modifié"
    assert data["city"] == "Paris"


def test_update_event_returns_404_when_not_found():
    response = client.patch(
        "/api/v1/events/00000000-0000-0000-0000-000000000000",
        json={"title": "Event modifié"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_delete_event():
    create_response = client.post(
        "/api/v1/events",
        json={
            "title": "Event à supprimer",
            "description": "Description",
            "event_type": "NEWS",
            "event_date": "2026-12-01T12:00:00Z",
        },
    )

    event_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/events/{event_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/api/v1/events/{event_id}")

    assert get_response.status_code == 404