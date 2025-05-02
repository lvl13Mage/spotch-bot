import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

export function TwitchSettings() {
  const [client_id, setClientId] = useState("");
  const [client_secret, setClientSecret] = useState("");
  const [scope, setScopes] = useState("");
  const [redirect_uri, setRedirectUri] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [isEditable, setIsEditable] = useState(false);
  const [showClientId, setShowClientId] = useState(false); // Toggle visibility for client_id
  const [showClientSecret, setShowClientSecret] = useState(false); // Toggle visibility for client_secret

  useEffect(() => {
    // Fetch existing credentials from the backend
    fetch("/credentials/twitch/credentials")
      .then((res) => res.json())
      .then((data) => {
        setClientId(data?.client_id || "");
        setClientSecret(data?.client_secret || "");
        setScopes(data?.scope || "channel:read:redemptions channel:manage:redemptions channel:read:subscriptions chat:read chat:edit user:write:chat user:read:chat user:bot channel:bot"); // Default scopes
        setRedirectUri(data?.redirect_uri || "http://127.0.0.1:8135/auth/twitch/callback");
      });
  }, []);

  const handleSave = async () => {
    if (!client_id || !client_secret || !scope || !redirect_uri) return;

    setIsSaving(true);
    await fetch("/credentials/twitch/set", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ client_id, client_secret, scope, redirect_uri }),
    });
    setIsSaving(false);
  };

  const handleAuthenticate = async () => {
    await handleSave();

    const response = await fetch("/auth/twitch", { method: "GET" });
    const data = await response.json();

    if (data.auth_url) {
      window.open(data.auth_url, "_blank"); // Open auth URL in a new tab
    } else {
      alert("Failed to retrieve Twitch authentication URL.");
    }
  };

  const handleDelete = async () => {
    const confirmed = window.confirm("Are you sure you want to delete Twitch credentials?");
    if (!confirmed) return;

    const response = await fetch("/credentials/twitch/delete", { method: "DELETE" });
    const data = await response.json();

    if (data.message) {
      alert(data.message);
      setClientId("");
      setClientSecret("");
      setScopes("channel:read:redemptions channel:manage:redemptions channel:read:subscriptions chat:read chat:edit user:write:chat user:read:chat user:bot channel:bot"); // Reset to default scopes
      setRedirectUri("http://127.0.0.1:8135/auth/twitch/callback");
    }
  };

  const isFormValid = client_id && client_secret && scope && redirect_uri;

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-lg font-semibold">Twitch Settings</h1>
      <div className="space-y-2">
        <label className="block relative">
          <span className="text-sm">Client ID</span>
          <div className="relative">
            <input
              type={showClientId ? "text" : "password"}
              value={client_id}
              onChange={(e) => setClientId(e.target.value)}
              className="w-full px-3 py-2 border rounded-md pr-10" // Add padding to the right for the icon
            />
            <button
              type="button"
              onClick={() => setShowClientId(!showClientId)}
              className="absolute inset-y-0 right-2 flex items-center text-gray-500 hover:text-gray-700"
              aria-label="Toggle Client ID Visibility"
            >
              <FontAwesomeIcon icon={showClientId ? faEyeSlash : faEye} />
            </button>
          </div>
        </label>
        <label className="block relative">
          <span className="text-sm">Client Secret</span>
          <div className="relative">
            <input
              type={showClientSecret ? "text" : "password"}
              value={client_secret}
              onChange={(e) => setClientSecret(e.target.value)}
              className="w-full px-3 py-2 border rounded-md pr-10" // Add padding to the right for the icon
            />
            <button
              type="button"
              onClick={() => setShowClientSecret(!showClientSecret)}
              className="absolute inset-y-0 right-2 flex items-center text-gray-500 hover:text-gray-700"
              aria-label="Toggle Client Secret Visibility"
            >
              <FontAwesomeIcon icon={showClientSecret ? faEyeSlash : faEye} />
            </button>
          </div>
        </label>
        <label className="block relative">
          <span className="text-sm flex items-center">
            Scopes
            <div className="relative group ml-2">
              <span
                className="text-blue-500 cursor-pointer text-xl"
                role="button"
                aria-label="Info about scopes"
                onClick={(e) => e.stopPropagation()} // Prevents checkbox toggle
              >
                &#9432;
              </span>
              <div className="absolute left-0 mt-1 hidden w-64 p-2 text-sm text-white bg-gray-800 rounded-md shadow-lg group-hover:block">
                Changing this may break the app. Ensure you know what you're doing.
              </div>
            </div>
          </span>
          <div className="mt-2 flex items-center gap-2">
            <input
              type="checkbox"
              id="editScopes"
              onChange={(e) => setIsEditable(e.target.checked)}
              className="cursor-pointer"
            />
            <label htmlFor="editScopes" className="text-sm cursor-pointer">
              Enable editing
            </label>
          </div>
          <input
            type="text"
            value={scope}
            onChange={(e) => setScopes(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            disabled={!isEditable}
          />
        </label>
        <label className="block">
          <span className="text-sm">Redirect URI</span>
          <input
            type="text"
            value={redirect_uri}
            onChange={(e) => setRedirectUri(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          />
        </label>
      </div>
      <div className="flex items-center gap-2">
        <button
          onClick={handleSave}
          disabled={!isFormValid || isSaving}
          className={`px-4 py-2 rounded-md text-white font-semibold transition-all duration-200 ${
            isSaving
              ? "bg-gray-400 cursor-not-allowed"
              : isFormValid
              ? "bg-blue-500 hover:bg-blue-600 active:bg-blue-700"
              : "bg-gray-400 cursor-not-allowed"
          }`}
        >
          {isSaving ? "Saving..." : "Save"}
        </button>
        <button
          onClick={handleAuthenticate}
          disabled={!isFormValid || isSaving}
          className={`px-4 py-2 rounded-md text-white font-semibold transition-all duration-200 ${
            isSaving
              ? "bg-gray-400 cursor-not-allowed"
              : isFormValid
              ? "bg-green-500 hover:bg-green-600 active:bg-green-700"
              : "bg-gray-400 cursor-not-allowed"
          }`}
        >
          Authenticate
        </button>
        <button
          onClick={handleDelete}
          className="px-4 py-2 rounded-md text-white font-semibold bg-red-500 hover:bg-red-600 active:bg-red-700 transition-all duration-200"
        >
          Delete
        </button>
      </div>
    </div>
  );
}