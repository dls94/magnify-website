import type { Release } from '../../types/release'
import { apiGet } from './client'

export function getReleases(): Promise<Release[]> {
  return apiGet<Release[]>('/releases')
}