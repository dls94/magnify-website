import { describe, expect, it, vi } from 'vitest'
import { getUpcomingEvents } from './events'

describe('getUpcomingEvents', () => {
  it('récupère les événements à venir', async () => {
    const events = [
      {
        id: '123',
        title: 'Magnify Live',
        description: 'Concert Magnify',
        event_type: 'CONCERT',
        event_date: '2026-10-10T20:00:00+02:00',
        artist_id: 'artist-123',
        venue_name: 'La Cigale',
        city: 'Paris',
        ticket_url: null,
        cover_image_url: null,
        is_published: true,
      },
    ]

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue(events),
      }),
    )

    await expect(getUpcomingEvents()).resolves.toEqual(events)

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/events/upcoming'),
      expect.objectContaining({
        method: 'GET',
      }),
    )
  })
})