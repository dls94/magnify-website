// src/types/auth.ts

export type UserRole = 'ADMIN' | 'ARTIST'

export interface AuthenticatedUser {
  id: string
  email: string
  role: UserRole
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: AuthenticatedUser
}