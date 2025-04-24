import { useState } from "react";
import axios from "axios";

const Auth = () => {
  const [twitchAuthUrl, setTwitchAuthUrl] = useState<string | null>(null);
  const [spotifyAuthUrl, setSpotifyAuthUrl] = useState<string | null>(null);

  const fetchTwitchAuthUrl = async () => {
    try {
      const response = await axios.get("/auth/twitch");
      setTwitchAuthUrl(response.data.auth_url);
    } catch (error) {
      console.error("Failed to fetch Twitch auth URL:", error);
    }
  };

  const fetchSpotifyAuthUrl = async () => {
    try {
      const response = await axios.get("/auth/spotify/authorize");
      setSpotifyAuthUrl(response.data.auth_url);
    } catch (error) {
      console.error("Failed to fetch Spotify auth URL:", error);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Authentication</h1>
      <div className="mb-4">
        <button
          onClick={fetchTwitchAuthUrl}
          className="bg-purple-500 text-white px-4 py-2 mr-2"
        >
          Authenticate with Twitch
        </button>
        {twitchAuthUrl && (
          <a
            href={twitchAuthUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 underline"
          >
            Complete Twitch Authentication
          </a>
        )}
      </div>
      <div className="mb-4">
        <button
          onClick={fetchSpotifyAuthUrl}
          className="bg-green-500 text-white px-4 py-2 mr-2"
        >
          Authenticate with Spotify
        </button>
        {spotifyAuthUrl && (
          <a
            href={spotifyAuthUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 underline"
          >
            Complete Spotify Authentication
          </a>
        )}
      </div>
    </div>
  );
};

export default Auth;