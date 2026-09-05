from datetime import UTC, datetime
from uuid import UUID

import pytest

from domain.models.artist import Artist


def test_artist_require_a_name():
    with pytest.raises(ValueError):
        Artist(name="",)

def test_artist_reject_blank_name():
    with pytest.raises(ValueError):
        Artist(name="  ",)

def test_artist_has_an_id():
    artist = Artist(name="Test Artist")

    assert isinstance(artist.id, UUID)

def test_artist_can_be_created_without_optional_information():
    artist = Artist(name="Test Artist",)

    assert artist.name == "Test Artist"
    assert artist.bio is None
    assert artist.picture_url is None
    assert artist.spotify_url is None
    assert artist.instagram_url is None

def test_artist_profile_is_incomplete_without_bio():
    artist = Artist(
        name="Test Artist",
        picture_url="https://example.com/artist.jpg",
    )

    assert artist.is_profile_complete() is False


def test_artist_profile_is_incomplete_without_picture():
    artist = Artist(
        name="Test Artist",
        bio="A great artist.",
    )

    assert artist.is_profile_complete() is False


def test_artist_profile_is_complete():
    artist = Artist(
        name="Test Artist",
        bio="A great artist.",
        picture_url="https://example.com/artist.jpg",
    )

    assert artist.is_profile_complete() is True


def test_artist_accepts_valid_spotify_url():
    artist = Artist(
        name="Test Artist",
    )

    artist.update_social_links(
        spotify_url="https://open.spotify.com/artist/123"
    )

    assert artist.spotify_url == "https://open.spotify.com/artist/123"


def test_artist_rejects_invalid_spotify_url():
    artist = Artist(
        name="Test Artist",
    )

    with pytest.raises(ValueError, match="URL Spotify est invalide"):
        artist.update_social_links(
            spotify_url="https://example.com/artist"
        )

def test_artist_has_creation_date():
    artist = Artist(
        name="Test Artist",
    )

    assert isinstance(artist.created_at, datetime)
    assert artist.created_at.tzinfo == UTC

def test_artist_can_update_social_links():
    artist = Artist(
        name="Test Artist",
    )

    artist.update_social_links(
        spotify_url="https://open.spotify.com/artist/123",
        instagram_url="https://instagram.com/testartist",
    )

    assert artist.spotify_url == "https://open.spotify.com/artist/123"
    assert artist.instagram_url == "https://instagram.com/testartist"

def test_artist_keeps_existing_social_links_when_not_updated():
    artist = Artist(
        name="Test Artist",
        instagram_url="https://instagram.com/testartist",
    )

    artist.update_social_links(
        spotify_url="https://open.spotify.com/artist/123",
    )

    assert artist.spotify_url == "https://open.spotify.com/artist/123"
    assert artist.instagram_url == "https://instagram.com/testartist"

def test_artist_can_update_profile():
    artist = Artist(
        name="Ancien nom",
        bio="Ancienne bio",
        picture_url="https://example.com/old.jpg",
        spotify_url="https://open.spotify.com/artist/old",
        instagram_url="https://instagram.com/old",
    )

    artist.update_profile(
        name="Nouveau nom",
        bio="Nouvelle bio",
        picture_url="https://example.com/new.jpg",
        spotify_url="https://open.spotify.com/artist/new",
        instagram_url="https://instagram.com/new",
    )

    assert artist.name == "Nouveau nom"
    assert artist.bio == "Nouvelle bio"
    assert artist.picture_url == "https://example.com/new.jpg"
    assert artist.spotify_url == "https://open.spotify.com/artist/new"
    assert artist.instagram_url == "https://instagram.com/new"


def test_artist_update_profile_keeps_omitted_fields():
    artist = Artist(
        name="Artiste",
        bio="Ma bio",
        picture_url="https://example.com/photo.jpg",
    )

    artist.update_profile(name="Nouveau nom")

    assert artist.name == "Nouveau nom"
    assert artist.bio == "Ma bio"
    assert artist.picture_url == "https://example.com/photo.jpg"


def test_artist_update_profile_rejects_blank_name():
    artist = Artist(name="Artiste")

    with pytest.raises(ValueError, match="nom"):
        artist.update_profile(name="   ")


def test_artist_update_profile_rejects_invalid_spotify_url():
    artist = Artist(name="Artiste")

    with pytest.raises(ValueError, match="Spotify"):
        artist.update_profile(
            spotify_url="https://youtube.com/artist"
        )