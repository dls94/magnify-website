import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import EventCard from './EventCard'

const event = {
  id: 'event-1',
  title: 'Magnify Live',
  description: 'Une soirée live Magnify Music.',
  event_type: 'CONCERT' as const,
  event_date: '2026-06-20T20:00:00',
  artist_id: 'artist-1',
  venue_name: 'La Maroquinerie',
  city: 'Paris',
  ticket_url: 'https://example.com/tickets',
  cover_image_url: 'https://example.com/magnify-live.jpg',
  is_published: true,
}

describe('EventCard', () => {
  it('affiche les informations principales de l’événement', () => {
    render(<EventCard event={event} />)

    expect(
      screen.getByRole('heading', { name: 'Magnify Live' }),
    ).toBeInTheDocument()

    expect(screen.getByText('CONCERT')).toBeInTheDocument()
    expect(screen.getByText('La Maroquinerie')).toBeInTheDocument()
    expect(screen.getByText('Paris')).toBeInTheDocument()
  })

  it('affiche la description quand elle existe', () => {
    render(<EventCard event={event} />)

    expect(
      screen.getByText('Une soirée live Magnify Music.'),
    ).toBeInTheDocument()
  })

  it('affiche l’image quand elle existe', () => {
    render(<EventCard event={event} />)

    expect(
      screen.getByRole('img', { name: 'Magnify Live' }),
    ).toHaveAttribute('src', event.cover_image_url)
  })

  it('affiche le lien de billetterie quand il existe', () => {
    render(<EventCard event={event} />)

    expect(
      screen.getByRole('link', { name: /billetterie/i }),
    ).toHaveAttribute('href', event.ticket_url)
  })

  it('n’affiche pas de lien de billetterie sans ticket_url', () => {
    render(
      <EventCard
        event={{
          ...event,
          ticket_url: null,
        }}
      />,
    )

    expect(
      screen.queryByRole('link', { name: /billetterie/i }),
    ).not.toBeInTheDocument()
  })
})