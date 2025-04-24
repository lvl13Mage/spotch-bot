import { useState } from "react";
import axios from "axios";

const SongRequests = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const searchSong = async () => {
    const response = await axios.get(`/api/song-requests/search?query=${query}`);
    setResults(response.data);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Song Requests</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search Song"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-2 mr-2"
        />
        <button onClick={searchSong} className="bg-blue-500 text-white px-4 py-2">
          Search
        </button>
      </div>
      <ul>
        {results.map((song: any) => (
          <li key={song.id}>{song.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default SongRequests;