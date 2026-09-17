import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import Home from "./Home";

vi.mock("../../services/api/artists", () => ({
  getArtists: vi.fn().mockResolvedValue([
    {
      id: "artist-1",
      name: "Echo Urbain",
      bio: "Artiste indépendant.",
      spotify_url: "https://open.spotify.com/artist/artist-1",
      instagram_url: "https://instagram.com/echo-urbain",
      picture_url: "https://example.com/echo-urbain.jpg",
    },
  ]),
}));

vi.mock("../../services/api/releases", () => ({
  getReleases: vi.fn().mockResolvedValue([
    {
      id: "release-1",
      title: "Horizons",
      artist_id: "artist-1",
      release_type: "ALBUM",
      release_date: "2026-03-15",
      cover_url: "https://example.com/horizons.jpg",
    },
  ]),
}));

vi.mock("../../services/api/events", () => ({
  getUpcomingEvents: vi.fn().mockResolvedValue([
    {
      id: "event-1",
      title: "Magnify Live",
      description: "Une soirée live Magnify Music.",
      event_type: "CONCERT",
      event_date: "2026-06-20T20:00:00",
      artist_id: "artist-1",
      venue_name: "La Maroquinerie",
      city: "Paris",
      ticket_url: "https://example.com/tickets",
      cover_image_url: "https://example.com/magnify-live.jpg",
      is_published: true,
    },
  ]),
}));

function renderHome() {
  return render(
    <MemoryRouter>
      <Home />
    </MemoryRouter>,
  );
}

describe("Home", () => {
  it("affiche le titre principal de Magnify Music", () => {
    renderHome();

    expect(
      screen.getByRole("heading", {
        name: /magnify music/i,
        level: 1,
      }),
    ).toBeInTheDocument();
  });

  it("affiche les sections principales", async () => {
    renderHome();

    expect(
      await screen.findByRole("heading", { name: /artistes/i }),
    ).toBeInTheDocument();

    expect(
      await screen.findByRole("heading", { name: /releases/i }),
    ).toBeInTheDocument();

    expect(
      await screen.findByRole("heading", { name: /événements/i }),
    ).toBeInTheDocument();
  });

  it("charge les données depuis les services API", async () => {
    const { getArtists } = await import("../../services/api/artists");
    const { getReleases } = await import("../../services/api/releases");
    const { getUpcomingEvents } = await import("../../services/api/events");

    renderHome();

    await screen.findByRole("heading", {
      name: /magnify music/i,
    });

    expect(getArtists).toHaveBeenCalledTimes(1);
    expect(getReleases).toHaveBeenCalledTimes(1);
    expect(getUpcomingEvents).toHaveBeenCalledTimes(1);
  });

  it("affiche les artistes récupérés", async () => {
    renderHome();

    expect(
      await screen.findByRole("heading", { name: "Echo Urbain" }),
    ).toBeInTheDocument();

    expect(screen.getByText("Artiste indépendant.")).toBeInTheDocument();
  });

  it("affiche le Hero", () => {
    renderHome();

    expect(
      screen.getByRole("heading", {
        name: /magnify music/i,
        level: 1,
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("link", {
        name: /découvrir les artistes/i,
      }),
    ).toHaveAttribute("href", "/artists");
  });

  it("affiche les releases récupérés", async () => {
    renderHome();

    expect(
      await screen.findByRole("heading", { name: "Horizons" }),
    ).toBeInTheDocument();
  });

  it("affiche les événements récupérés", async () => {
    renderHome();

    expect(
      await screen.findByRole("heading", { name: "Magnify Live" }),
    ).toBeInTheDocument();
  });
});
