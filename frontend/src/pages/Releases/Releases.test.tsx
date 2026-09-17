import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import Releases from './Releases'

vi.mock('../../services/api/releases', () => ({
  getReleases: vi.fn().mockResolvedValue([
    {
      id: 'release-1',
      title: 'Horizons',
      artist_id: 'artist-1',
      release_type: 'ALBUM',
      release_date: '2026-03-15',
      cover_url: 'https://example.com/horizons.jpg',
    },
    {
      id: 'release-2',
      title: 'Nuit Blanche',
      artist_id: 'artist-2',
      release_type: 'SINGLE',
      release_date: '2026-04-01',
      cover_url: null,
    },
  ]),
}))

describe('Releases', () => {
  it('affiche le titre de la page', () => {
    render(<Releases />)

    expect(
      screen.getByRole('heading', { name: /releases/i, level: 1 }),
    ).toBeInTheDocument()
  })

  it('affiche les releases récupérés depuis l’API', async () => {
    render(<Releases />)

    expect(
      await screen.findByRole('heading', { name: 'Horizons' }),
    ).toBeInTheDocument()

    expect(
      await screen.findByRole('heading', { name: 'Nuit Blanche' }),
    ).toBeInTheDocument()
  })
})