from uuid import UUID
import pytest
from application.use_cases.artist.update_artist import UpdateArtist
from domain.models.artist import Artist
from tests.fakes.artist_repository import InMemoryArtistRepository


def test_update_artist_updates_and_saves_artist():
    repository = InMemoryArtistRepository()
    artist = Artist(
        name="Ancien nom",
        bio="Ancienne bio",
    )
    repository.save(artist)

    use_case = UpdateArtist(repository)

    updated_artist = use_case.execute(
        artist_id=artist.id,
        name="Nouveau nom",
        bio="Nouvelle bio",
    )

    assert updated_artist.name == "Nouveau nom"
    assert updated_artist.bio == "Nouvelle bio"

    saved_artist = repository.get_by_id(artist.id)

    assert saved_artist is not None
    assert saved_artist.name == "Nouveau nom"
    assert saved_artist.bio == "Nouvelle bio"


def test_update_artist_returns_none_when_artist_does_not_exist():
    repository = InMemoryArtistRepository()
    use_case = UpdateArtist(repository)

    artist_id = UUID("12345678-1234-5678-1234-567812345678")

    result = use_case.execute(
        artist_id=artist_id,
        name="Nouveau nom",
    )

    assert result is None


def test_update_artist_rejects_invalid_profile_data():
    repository = InMemoryArtistRepository()
    artist = Artist(name="Artiste")
    repository.save(artist)

    use_case = UpdateArtist(repository)

    with pytest.raises(ValueError, match="nom"):
        use_case.execute(
            artist_id=artist.id,
            name="   ",
        )