import { Link } from 'react-router-dom'

import './Hero.css'

function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-heading">
      <div className="hero__inner">
        <p className="hero__eyebrow">Label indépendant</p>

        <h1 id="hero-heading">Magnify Music</h1>

        <p className="hero__description">
          Un label indépendant dédié aux artistes et à leurs projets musicaux.
        </p>

        <Link className="hero__cta" to="/artists">
          Découvrir les artistes
        </Link>
      </div>
    </section>
  )
}

export default Hero