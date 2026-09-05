from uuid import UUID

import pytest

from application.use_cases.artist.update_artist import UpdateArtist
from domain.models.artist import Artist
from tests.fakes.artist_repository import InMemoryArtistRepository


async def test_update_artist_updates_and_saves_artist():
    repository = InMemoryArtistRepository()
    artist = Artist(
        name="Ancien nom",
        bio="Ancienne bio",
    )
    await repository.save(artist)

    use_case = UpdateArtist(repository)

    updated_artist = await use_case.execute(
        artist_id=artist.id,
        name="Nouveau nom",
        bio="Nouvelle bio",
    )

    assert updated_artist is not None
    assert updated_artist.name == "Nouveau nom"
    assert updated_artist.bio == "Nouvelle bio"

    saved_artist = await repository.get_by_id(artist.id)

    assert saved_artist is not None
    assert saved_artist.name == "Nouveau nom"
    assert saved_artist.bio == "Nouvelle bio"


async def test_update_artist_returns_none_when_artist_does_not_exist():
    repository = InMemoryArtistRepository()
    use_case = UpdateArtist(repository)

    artist_id = UUID("12345678-1234-5678-1234-567812345678")

    result = await use_case.execute(
        artist_id=artist_id,
        name="Nouveau nom",
    )

    assert result is None


async def test_update_artist_rejects_invalid_profile_data():
    repository = InMemoryArtistRepository()
    artist = Artist(name="Artiste")
    await repository.save(artist)

    use_case = UpdateArtist(repository)

    with pytest.raises(ValueError, match="nom"):
        await use_case.execute(
            artist_id=artist.id,
            name="   ",
        )