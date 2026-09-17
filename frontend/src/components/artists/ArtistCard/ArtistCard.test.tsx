import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import ArtistCard from './ArtistCard'

const artist = {
  id: 'artist-1',
  name: 'Echo Urbain',
  bio: 'Artiste indépendant.',
  spotify_url: 'https://open.spotify.com/artist/artist-1',
  instagram_url: 'https://instagram.com/echo-urbain',
  picture_url: 'https://example.com/echo-urbain.jpg',
}

describe('ArtistCard', () => {
  it('affiche les informations principales de l’artiste', () => {
    render(<ArtistCard artist={artist} />)

    expect(
      screen.getByRole('heading', { name: 'Echo Urbain' }),
    ).toBeInTheDocument()

    expect(screen.getByText('Artiste indépendant.')).toBeInTheDocument()

    expect(
      screen.getByRole('img', { name: 'Echo Urbain' }),
    ).toHaveAttribute('src', artist.picture_url)
  })

  it('expose les liens Spotify et Instagram lorsqu’ils existent', () => {
    render(<ArtistCard artist={artist} />)

    expect(screen.getByRole('link', { name: /spotify/i })).toHaveAttribute(
      'href',
      artist.spotify_url,
    )

    expect(screen.getByRole('link', { name: /instagram/i })).toHaveAttribute(
      'href',
      artist.instagram_url,
    )
  })
})