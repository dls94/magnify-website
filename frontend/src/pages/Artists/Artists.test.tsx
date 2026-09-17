import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import Artists from './Artists'

vi.mock('../../services/api/artists', () => ({
  getArtists: vi.fn().mockResolvedValue([
    {
      id: 'artist-1',
      name: 'Echo Urbain',
      bio: 'Artiste indépendant.',
      spotify_url: null,
      instagram_url: null,
      picture_url: 'https://example.com/echo-urbain.jpg',
    },
    {
      id: 'artist-2',
      name: 'Magnify Soul',
      bio: 'Projet soul.',
      spotify_url: null,
      instagram_url: null,
      picture_url: null,
    },
  ]),
}))

describe('Artists', () => {
  it('affiche le titre de la page', async () => {
    render(<Artists />)

    expect(
      await screen.findByRole('heading', {
        name: /artistes/i,
        level: 1,
      }),
    ).toBeInTheDocument()
  })

  it('affiche les artistes récupérés depuis l’API', async () => {
    render(<Artists />)

    expect(
      await screen.findByRole('heading', {
        name: 'Echo Urbain',
      }),
    ).toBeInTheDocument()

    expect(
      await screen.findByRole('heading', {
        name: 'Magnify Soul',
      }),
    ).toBeInTheDocument()
  })
})