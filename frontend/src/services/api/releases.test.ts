import { describe, expect, it, vi } from 'vitest'
import { getReleases } from './releases'

describe('getReleases', () => {
  it('récupère la liste des sorties', async () => {
    const releases = [
      {
        id: '123',
        title: 'Écho Urbain',
        artist_id: 'artist-123',
        release_type: 'SINGLE',
        release_date: '2026-09-01',
        cover_url: null,
      },
    ]

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue(releases),
      }),
    )

    await expect(getReleases()).resolves.toEqual(releases)

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/releases'),
      expect.objectContaining({
        method: 'GET',
      }),
    )
  })
})