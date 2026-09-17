import { describe, expect, it, vi } from 'vitest'
import { apiGet } from './client'

describe('apiGet', () => {
  it('appelle l’API et retourne les données JSON', async () => {
    const response = {
      id: '123',
      name: 'Magnify',
    }

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue(response),
      }),
    )

    await expect(apiGet('/artists/123')).resolves.toEqual(response)

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/artists/123'),
      expect.objectContaining({
        method: 'GET',
      }),
    )
  })
})