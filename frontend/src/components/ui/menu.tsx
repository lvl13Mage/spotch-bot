import { NavLink } from "react-router-dom";

export function Menu() {
  return (
    <nav className="p-4 space-y-6">
      {/* Main Links */}
      <div className="space-y-2">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `block px-4 py-2 rounded-md ${
              isActive ? "bg-primary text-primary-foreground" : "hover:bg-muted"
            }`
          }
        >
          Home
        </NavLink>
        <NavLink
          to="/rewards"
          className={({ isActive }) =>
            `block px-4 py-2 rounded-md ${
              isActive ? "bg-primary text-primary-foreground" : "hover:bg-muted"
            }`
          }
        >
          Rewards
        </NavLink>
        <NavLink
          to="/song-requests"
          className={({ isActive }) =>
            `block px-4 py-2 rounded-md ${
              isActive ? "bg-primary text-primary-foreground" : "hover:bg-muted"
            }`
          }
        >
          Song Requests
        </NavLink>
      </div>

      {/* Settings Section */}
      <div className="space-y-2">
        <h3 className="text-sm font-semibold text-muted-foreground">Settings</h3>
        <hr className="border-border" />
        <NavLink
          to="/settings/spotify"
          className={({ isActive }) =>
            `block px-4 py-2 rounded-md ${
              isActive ? "bg-primary text-primary-foreground" : "hover:bg-muted"
            }`
          }
        >
          Spotify
        </NavLink>
        <NavLink
          to="/settings/twitch"
          className={({ isActive }) =>
            `block px-4 py-2 rounded-md ${
              isActive ? "bg-primary text-primary-foreground" : "hover:bg-muted"
            }`
          }
        >
          Twitch
        </NavLink>
      </div>
    </nav>
  );
}