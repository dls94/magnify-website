import type { Artist } from '../../types/artist'
import { apiGet } from './client'

export function getArtists(): Promise<Artist[]> {
  return apiGet<Artist[]>('/artists')
}