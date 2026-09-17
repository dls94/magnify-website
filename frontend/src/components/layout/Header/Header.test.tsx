import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { MemoryRouter } from 'react-router-dom'

import Header from './Header'

describe('Header', () => {
  it('affiche le logo Magnify Music', () => {
    render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>,
    )

    expect(screen.getByRole('link', { name: /magnify music/i })).toBeInTheDocument()
  })

  it('affiche la navigation principale', () => {
    render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>,
    )

    expect(screen.getByRole('link', { name: /accueil/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /artistes/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /releases/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /événements/i })).toBeInTheDocument()
  })

  it('marque la page courante comme active', () => {
    render(
      <MemoryRouter initialEntries={['/artists']}>
        <Header />
      </MemoryRouter>,
    )

    expect(screen.getByRole('link', { name: /artistes/i })).toHaveAttribute(
      'aria-current',
      'page',
    )
  })

  it('utilise la structure du header prévue par le design', () => {
  render(
    <MemoryRouter>
      <Header />
    </MemoryRouter>,
  )

  expect(document.querySelector('.site-header')).toBeInTheDocument()
  expect(document.querySelector('.site-header__inner')).toBeInTheDocument()
  expect(document.querySelector('.site-header__logo')).toBeInTheDocument()
  expect(document.querySelector('.site-header__nav')).toBeInTheDocument()
  })

  it('affiche un bouton de menu sur mobile', () => {
  render(
    <MemoryRouter>
      <Header />
    </MemoryRouter>,
  )

  expect(
    screen.getByRole('button', { name: /ouvrir le menu/i }),
  ).toBeInTheDocument()
})

it('masque la navigation mobile au chargement', () => {
  render(
    <MemoryRouter>
      <Header />
    </MemoryRouter>,
  )

  expect(
    screen.queryByRole('navigation', { name: /navigation mobile/i }),
  ).not.toBeInTheDocument()
})

it('affiche le logo Magnify Music comme image', () => {
  render(
    <MemoryRouter>
      <Header />
    </MemoryRouter>,
  )

  expect(
    screen.getByRole('img', { name: 'Magnify Music' }),
  ).toBeInTheDocument()
})
})