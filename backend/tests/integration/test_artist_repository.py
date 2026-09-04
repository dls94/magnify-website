from sqlalchemy import select

from domain.models.artist import Artist
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.models.artist import ArtistModel
from infrastructure.database.repositories.artist_repository import ArtistRepository
from uuid import uuid4

async def test_save_artist_persists_artist_in_database():
    artist = Artist(
        name="Integration Artist",
        bio="Artist created during integration test.",
        picture_url="https://example.com/artist.jpg",
    )

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        saved_artist = await repository.save(artist)

    assert saved_artist == artist

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArtistModel).where(ArtistModel.id == artist.id)
        )
        artist_model = result.scalar_one()

    assert artist_model.id == artist.id
    assert artist_model.name == "Integration Artist"
    assert artist_model.bio == "Artist created during integration test."
    assert artist_model.picture_url == "https://example.com/artist.jpg"

async def test_get_by_id_returns_existing_artist():
    artist = Artist(
        name="Get Artist",
        bio="Artist used for get test.",
        picture_url="https://example.com/get.jpg",
    )

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        await repository.save(artist)

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        result = await repository.get_by_id(artist.id)

    assert result == artist

async def test_get_by_id_returns_none_when_artist_does_not_exist():
    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        result = await repository.get_by_id(uuid4())

    assert result is None

async def test_list_all_returns_all_artists():
    artist_one = Artist(name="Artist One")
    artist_two = Artist(name="Artist Two")

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        await repository.save(artist_one)
        await repository.save(artist_two)

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        result = await repository.list_all()

    assert artist_one in result
    assert artist_two in result

async def test_save_existing_artist_updates_artist():
    artist = Artist(
        name="Original Name",
        bio="Original bio",
    )

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        await repository.save(artist)

    artist.name = "Updated Name"
    artist.bio = "Updated bio"

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        await repository.save(artist)

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        result = await repository.get_by_id(artist.id)

    assert result is not None
    assert result.name == "Updated Name"
    assert result.bio == "Updated bio"

async def test_delete_removes_artist():
    artist = Artist(name="Artist To Delete")

    async with AsyncSessionLocal() as session:
        repository = ArtistRepository(session)

        await repository.save(artist)

        deleted = await repository.delete(artist.id)

        assert deleted is True

        result = await repository.get_by_id(artist.id)

        assert result is None