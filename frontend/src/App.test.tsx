import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

vi.mock('./pages/Home/Home', () => ({
  default: () => <h1>Magnify Music</h1>,
}))

vi.mock('./pages/Artists/Artists', () => ({
  default: () => <h1>Artistes</h1>,
}))

vi.mock('./pages/Releases/Releases', () => ({
  default: () => <h1>Releases</h1>,
}))

vi.mock('./pages/Events/Events', () => ({
  default: () => <h1>Événements</h1>,
}))

import App from './App'

describe('App', () => {
  it('affiche la page d’accueil', () => {
    window.history.pushState({}, '', '/')

    render(<App />)

    expect(
      screen.getByRole('heading', {
        name: /magnify music/i,
      }),
    ).toBeInTheDocument()
  })

  it('affiche la page artistes', () => {
    window.history.pushState({}, '', '/artists')

    render(<App />)

    expect(
      screen.getByRole('heading', {
        name: /artistes/i,
      }),
    ).toBeInTheDocument()
  })
})