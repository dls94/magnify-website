// src/types/event.ts

export type EventType =
  | 'CONCERT'
  | 'FESTIVAL'
  | 'RELEASE_PARTY'
  | 'NEWS'

export interface Event {
  id: string
  title: string
  description: string
  event_type: EventType
  event_date: string
  artist_id: string | null
  venue_name: string | null
  city: string | null
  ticket_url: string | null
  cover_image_url: string | null
  is_published: boolean
}