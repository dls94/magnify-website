from uuid import UUID

from application.use_cases.artist.get_artist import GetArtist
from domain.models.artist import Artist
from tests.fakes.artist_repository import InMemoryArtistRepository


async def test_get_artist_returns_existing_artist():
    repository = InMemoryArtistRepository()
    artist = Artist(name="Zaidi")
    await repository.save(artist)

    use_case = GetArtist(repository)

    result = await use_case.execute(artist.id)

    assert result == artist


async def test_get_artist_returns_none_when_artist_does_not_exist():
    repository = InMemoryArtistRepository()
    use_case = GetArtist(repository)

    artist_id = UUID("12345678-1234-5678-1234-567812345678")

    result = await use_case.execute(artist_id)

    assert result is None