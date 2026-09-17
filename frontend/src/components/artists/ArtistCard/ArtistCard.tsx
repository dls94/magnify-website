import type { Artist } from '../../../types/artist'

type ArtistCardProps = {
  artist: Artist
}

function ArtistCard({ artist }: ArtistCardProps) {
  return (
    <article>
      {artist.picture_url && (
        <img src={artist.picture_url} alt={artist.name} />
      )}

      <h3>{artist.name}</h3>

      {artist.bio && <p>{artist.bio}</p>}

      <div>
        {artist.spotify_url && (
          <a
            href={artist.spotify_url}
            target="_blank"
            rel="noreferrer"
          >
            Spotify
          </a>
        )}

        {artist.instagram_url && (
          <a
            href={artist.instagram_url}
            target="_blank"
            rel="noreferrer"
          >
            Instagram
          </a>
        )}
      </div>
    </article>
  )
}

export default ArtistCard