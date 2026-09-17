import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { MemoryRouter } from 'react-router-dom'

import Hero from './Hero'

describe('Hero', () => {
  it('affiche le titre principal', () => {
    render(
      <MemoryRouter>
        <Hero />
      </MemoryRouter>,
    )

    expect(
      screen.getByRole('heading', {
        name: /magnify music/i,
        level: 1,
      }),
    ).toBeInTheDocument()
  })

  it('affiche une présentation du label', () => {
    render(
      <MemoryRouter>
        <Hero />
      </MemoryRouter>,
    )

    expect(
      screen.getByText('Label indépendant', { exact: true }),
    ).toBeInTheDocument()
  })

  it('propose un accès au catalogue des artistes', () => {
    render(
      <MemoryRouter>
        <Hero />
      </MemoryRouter>,
    )

    expect(
      screen.getByRole('link', { name: /découvrir les artistes/i }),
    ).toHaveAttribute('href', '/artists')
  })
})