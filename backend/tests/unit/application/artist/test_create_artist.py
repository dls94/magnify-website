from uuid import UUID

from domain.models.artist import Artist
from application.use_cases.artist.create_artist import CreateArtist
from tests.fakes.artist_repository import InMemoryArtistRepository


async def test_create_artist_creates_and_saves_artist():
    repository = InMemoryArtistRepository()
    use_case = CreateArtist(repository)

    artist = await use_case.execute(
        name="Zaidi",
        bio="A great artist.",
        picture_url="https://example.com/artist.jpg",
    )

    assert isinstance(artist, Artist)
    assert isinstance(artist.id, UUID)
    assert artist.name == "Zaidi"
    assert artist.bio == "A great artist."
    assert artist.picture_url == "https://example.com/artist.jpg"

    assert await repository.get_by_id(artist.id) == artist


async def test_create_artist_rejects_blank_name():
    repository = InMemoryArtistRepository()
    use_case = CreateArtist(repository)

    try:
        await use_case.execute(name="   ")
    except ValueError:
        pass
    else:
        raise AssertionError("Une erreur ValueError était attendue.")

    assert repository.artists == {}