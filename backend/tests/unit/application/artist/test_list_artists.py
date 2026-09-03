from domain.models.artist import Artist
from application.use_cases.artist.list_artists import ListArtists
from tests.fakes.artist_repository import InMemoryArtistRepository


def test_list_artists_returns_all_artists():
    repository = InMemoryArtistRepository()

    artist_1 = Artist(name="Zaidi")
    artist_2 = Artist(name="Test Artist")

    repository.save(artist_1)
    repository.save(artist_2)

    use_case = ListArtists(repository)

    result = use_case.execute()

    assert result == [artist_1, artist_2]


def test_list_artists_returns_empty_list_when_no_artists():
    repository = InMemoryArtistRepository()
    use_case = ListArtists(repository)

    result = use_case.execute()

    assert result == []