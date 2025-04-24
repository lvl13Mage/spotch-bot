import { useState, useEffect } from "react";

export function SpotifySettings() {
  const [credentials, setCredentials] = useState(null);
  const [clientId, setClientId] = useState("");
  const [clientSecret, setClientSecret] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    // Fetch existing credentials from the backend
    fetch("/api/spotify/credentials")
      .then((res) => res.json())
      .then((data) => {
        setCredentials(data);
        setClientId(data?.clientId || "");
        setClientSecret(data?.clientSecret || "");
      });
  }, []);

  const handleSave = async () => {
    setIsSaving(true);
    await fetch("/api/spotify/credentials", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clientId, clientSecret }),
    });
    setIsSaving(false);
  };

  const handleAuthenticate = async () => {
    if (!credentials) {
      await handleSave();
    }
    await fetch("/api/spotify/authenticate", { method: "POST" });
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-lg font-semibold">Spotify Settings</h1>
      <div className="space-y-2">
        <label className="block">
          <span className="text-sm">Client ID</span>
          <input
            type="text"
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          />
        </label>
        <label className="block">
          <span className="text-sm">Client Secret</span>
          <input
            type="password"
            value={clientSecret}
            onChange={(e) => setClientSecret(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          />
        </label>
      </div>
      <div className="flex items-center gap-2">
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="px-4 py-2 text-white bg-primary rounded-md disabled:opacity-50"
        >
          Save
        </button>
        <button
          onClick={handleAuthenticate}
          disabled={!clientId || !clientSecret || isSaving}
          className="px-4 py-2 text-white bg-secondary rounded-md disabled:opacity-50"
        >
          Authenticate
        </button>
      </div>
    </div>
  );
}