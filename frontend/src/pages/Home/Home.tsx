import { useEffect, useState } from "react";

import ArtistCard from "../../components/artists/ArtistCard/ArtistCard";
import EventCard from "../../components/events/EventCard/EventCard";
import ReleaseCard from "../../components/releases/ReleaseCard/ReleaseCard";
import Hero from "../../components/home/Hero/Hero";
import { getArtists } from "../../services/api/artists";
import { getUpcomingEvents } from "../../services/api/events";
import { getReleases } from "../../services/api/releases";
import type { Artist } from "../../types/artist";
import type { Event } from "../../types/event";
import type { Release } from "../../types/release";

function Home() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [releases, setReleases] = useState<Release[]>([]);
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    void Promise.all([
      getArtists().then(setArtists),
      getReleases().then(setReleases),
      getUpcomingEvents().then(setEvents),
    ]);
  }, []);

  return (
    <>
      <Hero />
      <section aria-labelledby="artists-heading">
        <h2 id="artists-heading">Artistes</h2>

        <div>
          {artists.map((artist) => (
            <ArtistCard key={artist.id} artist={artist} />
          ))}
        </div>
      </section>

      <section aria-labelledby="releases-heading">
        <h2 id="releases-heading">Releases</h2>

        <div>
          {releases.map((release) => (
            <ReleaseCard key={release.id} release={release} />
          ))}
        </div>
      </section>

      <section aria-labelledby="events-heading">
        <h2 id="events-heading">Événements</h2>

        <div>
          {events.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      </section>
    </>
  );
}

export default Home;
