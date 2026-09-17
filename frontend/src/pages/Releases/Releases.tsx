import { useEffect, useState } from 'react'

import ReleaseCard from '../../components/releases/ReleaseCard/ReleaseCard'
import { getReleases } from '../../services/api/releases'
import type { Release } from '../../types/release'

function Releases() {
  const [releases, setReleases] = useState<Release[]>([])

  useEffect(() => {
    void getReleases().then(setReleases)
  }, [])

  return (
    <main>
      <h1>Releases</h1>

      <section aria-label="Catalogue des releases">
        {releases.map((release) => (
          <ReleaseCard key={release.id} release={release} />
        ))}
      </section>
    </main>
  )
}

export default Releases