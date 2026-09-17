import { describe, expect, it, vi } from 'vitest'
import { getArtists } from './artists'

describe('getArtists', () => {
  it('récupère la liste des artistes', async () => {
    const artists = [
      {
        id: '123',
        name: 'Léo Disco',
        bio: null,
        spotify_url: null,
        instagram_url: null,
        picture_url: null,
      },
    ]

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue(artists),
      }),
    )

    await expect(getArtists()).resolves.toEqual(artists)

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/artists'),
      expect.objectContaining({
        method: 'GET',
      }),
    )
  })
})