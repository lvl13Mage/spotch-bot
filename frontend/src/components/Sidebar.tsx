import { NavLink } from "react-router-dom";
import { ModeToggle } from "@/components/ModeToggle";

const Sidebar = () => {
  return (
    <div className="h-screen w-64 bg-gray-900 text-white flex flex-col">
      {/* Header */}
      <div className="p-4 flex items-center justify-between border-b border-gray-700">
        <span className="text-lg font-bold">Spotify Bot</span>
        <ModeToggle />
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-4">
        {/* Main Links */}
        <div className="space-y-2">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `block px-4 py-2 rounded hover:bg-gray-700 ${
                isActive ? "bg-gray-700 text-white no-underline" : "text-white no-underline"
              }`
            }
          >
            Home
          </NavLink>
          <NavLink
            to="/rewards"
            className={({ isActive }) =>
              `block px-4 py-2 rounded hover:bg-gray-700 ${
                isActive ? "bg-gray-700 text-white no-underline" : "text-white no-underline"
              }`
            }
          >
            Rewards
          </NavLink>
          <NavLink
            to="/song-requests"
            className={({ isActive }) =>
              `block px-4 py-2 rounded hover:bg-gray-700 ${
                isActive ? "bg-gray-700 text-white no-underline" : "text-white no-underline"
              }`
            }
          >
            Song Requests
          </NavLink>
          <NavLink
            to="/auth"
            className={({ isActive }) =>
              `block px-4 py-2 rounded hover:bg-gray-700 ${
                isActive ? "bg-gray-700 text-white no-underline" : "text-white no-underline"
              }`
            }
          >
            Authentication
          </NavLink>
        </div>

        {/* Settings Section */}
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-gray-400">Settings</h3>
          <hr className="border-gray-700" />
          <NavLink
            to="/settings/spotify"
            className={({ isActive }) =>
              `block px-4 py-2 rounded hover:bg-gray-700 ${
                isActive ? "bg-gray-700 text-white no-underline" : "text-white no-underline"
              }`
            }
          >
            Spotify
          </NavLink>
          <NavLink
            to="/settings/twitch"
            className={({ isActive }) =>
              `block px-4 py-2 rounded hover:bg-gray-700 ${
                isActive ? "bg-gray-700 text-white no-underline" : "text-white no-underline"
              }`
            }
          >
            Twitch
          </NavLink>
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;