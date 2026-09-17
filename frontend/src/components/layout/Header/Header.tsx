import { useState } from 'react'
import { NavLink } from 'react-router-dom'

import logo from '../../../assets/logo.png'

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const closeMenu = () => {
    setIsMenuOpen(false)
  }

  return (
    <header className="site-header">
      <div className="site-header__inner">
        <NavLink className="site-header__logo" to="/" onClick={closeMenu}>
          <img src={logo} alt="Magnify Music" />
        </NavLink>

        <button
          className="site-header__menu-button"
          type="button"
          aria-label="Ouvrir le menu"
          aria-expanded={isMenuOpen}
          onClick={() => setIsMenuOpen((open) => !open)}
        >
          Menu
        </button>

        <nav
          className="site-header__nav"
          aria-label="Navigation principale"
        >
          <NavLink to="/" onClick={closeMenu}>
            Accueil
          </NavLink>
          <NavLink to="/artists" onClick={closeMenu}>
            Artistes
          </NavLink>
          <NavLink to="/releases" onClick={closeMenu}>
            Releases
          </NavLink>
          <NavLink to="/events" onClick={closeMenu}>
            Événements
          </NavLink>
        </nav>

        {isMenuOpen && (
          <nav
            className="site-header__mobile-nav"
            aria-label="Navigation mobile"
          >
            <NavLink to="/" onClick={closeMenu}>
              Accueil
            </NavLink>
            <NavLink to="/artists" onClick={closeMenu}>
              Artistes
            </NavLink>
            <NavLink to="/releases" onClick={closeMenu}>
              Releases
            </NavLink>
            <NavLink to="/events" onClick={closeMenu}>
              Événements
            </NavLink>
          </nav>
        )}
      </div>
    </header>
  )
}

export default Header