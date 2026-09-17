import { useEffect, useState } from 'react'

import ArtistCard from '../../components/artists/ArtistCard/ArtistCard'
import { getArtists } from '../../services/api/artists'
import type { Artist } from '../../types/artist'

function Artists() {
  const [artists, setArtists] = useState<Artist[]>([])

  useEffect(() => {
    void getArtists().then(setArtists)
  }, [])

  return (
    <main>
      <h1>Artistes</h1>

      <section aria-label="Catalogue des artistes">
        {artists.map((artist) => (
          <ArtistCard key={artist.id} artist={artist} />
        ))}
      </section>
    </main>
  )
}

export default Artists