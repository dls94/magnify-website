import { useEffect, useState } from 'react'

import EventCard from '../../components/events/EventCard/EventCard'
import { getUpcomingEvents } from '../../services/api/events'
import type { Event } from '../../types/event'

function Events() {
  const [events, setEvents] = useState<Event[]>([])

  useEffect(() => {
    void getUpcomingEvents().then(setEvents)
  }, [])

  return (
    <main>
      <h1>Événements</h1>

      <section aria-label="Agenda des événements">
        {events.map((event) => (
          <EventCard key={event.id} event={event} />
        ))}
      </section>
    </main>
  )
}

export default Events