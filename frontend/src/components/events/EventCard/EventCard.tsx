import type { Event } from '../../../types/event'

type EventCardProps = {
  event: Event
}

function formatEventDate(date: string): string {
  const eventDate = new Date(date)

  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(eventDate)
}

function EventCard({ event }: EventCardProps) {
  return (
    <article>
      {event.cover_image_url && (
        <img src={event.cover_image_url} alt={event.title} />
      )}

      <h2>{event.title}</h2>

      <p>{event.event_type}</p>

      <time dateTime={event.event_date}>
        {formatEventDate(event.event_date)}
      </time>

      {event.venue_name && <p>{event.venue_name}</p>}

      {event.city && <p>{event.city}</p>}

      {event.description && <p>{event.description}</p>}

      {event.ticket_url && (
        <a
          href={event.ticket_url}
          target="_blank"
          rel="noreferrer"
        >
          Billetterie
        </a>
      )}
    </article>
  )
}

export default EventCard