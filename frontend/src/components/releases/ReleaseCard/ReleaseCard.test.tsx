import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import ReleaseCard from './ReleaseCard'

const release = {
  id: 'release-1',
  title: 'Horizons',
  artist_id: 'artist-1',
  release_type: 'ALBUM' as const,
  release_date: '2026-03-15',
  cover_url: 'https://example.com/horizons.jpg',
}

describe('ReleaseCard', () => {
  it('affiche les informations principales du release', () => {
    render(<ReleaseCard release={release} />)

    expect(
      screen.getByRole('heading', { name: 'Horizons' }),
    ).toBeInTheDocument()

    expect(screen.getByText('ALBUM')).toBeInTheDocument()
    expect(screen.getByText('15/03/2026')).toBeInTheDocument()
  })

  it('affiche la cover quand elle existe', () => {
    render(<ReleaseCard release={release} />)

    expect(screen.getByRole('img', { name: 'Horizons' })).toHaveAttribute(
      'src',
      release.cover_url,
    )
  })

  it('n’affiche pas d’image quand aucune cover n’existe', () => {
    render(
      <ReleaseCard
        release={{
          ...release,
          cover_url: null,
        }}
      />,
    )

    expect(screen.queryByRole('img')).not.toBeInTheDocument()
  })
})