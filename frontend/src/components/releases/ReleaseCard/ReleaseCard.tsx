import type { Release } from '../../../types/release'

type ReleaseCardProps = {
  release: Release
}

function formatReleaseDate(date: string): string {
  const [year, month, day] = date.split('-')

  return `${day}/${month}/${year}`
}

function ReleaseCard({ release }: ReleaseCardProps) {
  return (
    <article>
      {release.cover_url && (
        <img src={release.cover_url} alt={release.title} />
      )}

      <h2>{release.title}</h2>

      <p>{release.release_type}</p>
      <time dateTime={release.release_date}>
        {formatReleaseDate(release.release_date)}
      </time>
    </article>
  )
}

export default ReleaseCard