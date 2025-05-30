import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Rewards from "./pages/Rewards";
import RewardForm from "./pages/RewardForm"; // Import the RewardForm component
import SongRequests from "./pages/SongRequests";
import Auth from "./pages/Auth";
import { SpotifySettings } from "./pages/settings/SpotifySettings";
import { TwitchSettings } from "./pages/settings/TwitchSettings";
import { ThemeProvider } from "@/components/ThemeProvider"; // Import ThemeProvider

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="spotify-bot-theme">
      <Router basename="/static">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="rewards" element={<Rewards />} />
            <Route path="rewards/add" element={<RewardForm />} /> {/* Add route for adding rewards */}
            <Route path="rewards/edit/:id" element={<RewardForm />} /> {/* Add route for editing rewards */}
            <Route path="song-requests" element={<SongRequests />} />
            <Route path="auth" element={<Auth />} />
            <Route path="settings/spotify" element={<SpotifySettings />} />
            <Route path="settings/twitch" element={<TwitchSettings />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
