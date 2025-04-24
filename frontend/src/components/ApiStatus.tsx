import React, { useState, useEffect } from "react";

const ApiStatus: React.FC = () => {
    const [twitchCredentialsSet, setTwitchCredentialsSet] = useState<boolean | null>(null);
    const [spotifyCredentialsSet, setSpotifyCredentialsSet] = useState<boolean | null>(null);

    useEffect(() => {
        // Fetch Twitch credentials status
        fetch("/credentials/status/twitch")
            .then((res) => res.json())
            .then((data) => setTwitchCredentialsSet(data.twitch_credentials_set))
            .catch((err) => console.error("Failed to fetch Twitch credentials status:", err));

        // Fetch Spotify credentials status
        fetch("/credentials/status/spotify")
            .then((res) => res.json())
            .then((data) => setSpotifyCredentialsSet(data.spotify_credentials_set))
            .catch((err) => console.error("Failed to fetch Spotify credentials status:", err));
    }, []);

    return (
        <div>
            <h2>API Status</h2>
            <div>
                <p>
                    <strong>Twitch Credentials:</strong>{" "}
                    {twitchCredentialsSet === null
                        ? "Loading..."
                        : twitchCredentialsSet
                        ? "✅ Set"
                        : "❌ Not Set"}
                </p>
                <p>
                    <strong>Spotify Credentials:</strong>{" "}
                    {spotifyCredentialsSet === null
                        ? "Loading..."
                        : spotifyCredentialsSet
                        ? "✅ Set"
                        : "❌ Not Set"}
                </p>
            </div>
        </div>
    );
};

export default ApiStatus;