import type { Event } from '../../types/event'
import { apiGet } from './client'

export function getUpcomingEvents(): Promise<Event[]> {
  return apiGet<Event[]>('/events/upcoming')
}