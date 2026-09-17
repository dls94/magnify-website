import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import Events from './Events'

vi.mock('../../services/api/events', () => ({
  getUpcomingEvents: vi.fn().mockResolvedValue([
    {
      id: 'event-1',
      title: 'Magnify Live',
      description: 'Une soirée live Magnify Music.',
      event_type: 'CONCERT',
      event_date: '2026-06-20T20:00:00',
      artist_id: 'artist-1',
      venue_name: 'La Maroquinerie',
      city: 'Paris',
      ticket_url: 'https://example.com/tickets',
      cover_image_url: 'https://example.com/magnify-live.jpg',
      is_published: true,
    },
    {
      id: 'event-2',
      title: 'Summer Festival',
      description: null,
      event_type: 'FESTIVAL',
      event_date: '2026-07-10T18:00:00',
      artist_id: null,
      venue_name: 'Parc Floral',
      city: 'Paris',
      ticket_url: null,
      cover_image_url: null,
      is_published: true,
    },
  ]),
}))

describe('Events', () => {
  it('affiche le titre de la page', () => {
    render(<Events />)

    expect(
      screen.getByRole('heading', { name: /événements/i, level: 1 }),
    ).toBeInTheDocument()
  })

  it('affiche les événements récupérés depuis l’API', async () => {
    render(<Events />)

    expect(
      await screen.findByRole('heading', { name: 'Magnify Live' }),
    ).toBeInTheDocument()

    expect(
      await screen.findByRole('heading', { name: 'Summer Festival' }),
    ).toBeInTheDocument()
  })
})