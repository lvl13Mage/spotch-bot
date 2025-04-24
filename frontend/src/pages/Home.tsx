import React from "react";
import ApiStatus from "@/components/ApiStatus";

const Home: React.FC = () => {
    return (
        <div>
            <h1>Welcome to Spotify-Twitch Bot</h1>
            <p>This is your dashboard where you can monitor API credentials and manage your bot.</p>
            <ApiStatus />
        </div>
    );
};

export default Home;