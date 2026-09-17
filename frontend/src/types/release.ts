// src/types/release.ts

export type ReleaseType = 'SINGLE' | 'EP' | 'ALBUM'

export interface Release {
  id: string
  title: string
  artist_id: string | null
  release_type: ReleaseType
  release_date: string
  cover_url: string | null
}