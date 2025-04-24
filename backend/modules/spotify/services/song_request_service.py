from backend.modules.spotify.spotify_client import SpotifyClient
from backend.modules.database.database import get_db_sync
import re

class SongRequestService:
    def __init__(self):
        self.db = get_db_sync()
        self.spotify_client = SpotifyClient(self.db)

    def search_song(self, query: str, items: int = 1):
        """
        Search for a song on Spotify.
        Differentiates between Spotify URI, Spotify URL, and full-text search.
        """
        print(f"Searching for song: {query}")

        # Check if the query is a Spotify URI
        if re.match(r"^spotify:track:[a-zA-Z0-9]+$", query):
            print("Query is a Spotify URI.")
            return self._get_song_by_uri(query)

        # Check if the query is a Spotify URL
        elif re.match(r"^https?://open\.spotify\.com(/[\w-]+)?/track/[a-zA-Z0-9]+", query):
            print("Query is a Spotify URL.")
            return self._get_song_by_url(query)

        # Otherwise, perform a full-text search
        else:
            print("Query is a full-text search.")
            return self._search_song_by_text(query, items)

    def _get_song_by_uri(self, uri: str):
        """Retrieve a song by its Spotify URI."""
        try:
            track_id = uri.split(":")[-1]
            track = self.spotify_client.sp.track(track_id)
            return [self._get_song_result(track)]
        except Exception as e:
            print(f"Error retrieving song by URI: {e}")
            return None

    def _get_song_by_url(self, url: str):
        """Retrieve a song by its Spotify URL."""
        try:
            track_id = url.split("/")[-1].split("?")[0]
            track = self.spotify_client.sp.track(track_id)
            return [self._get_song_result(track)]
        except Exception as e:
            print(f"Error retrieving song by URL: {e}")
            return None

    def _search_song_by_text(self, text: str, items: int = 1):
        """Perform a full-text search for a song."""
        try:
            results = self.spotify_client.sp.search(q=text, type='track')
            if results['tracks']['items']:
                formated_results = []
                for result in results['tracks']['items'][:items]:
                    formated_result = self._get_song_result(result)
                    formated_results.append(formated_result)
                return formated_results
            else:
                print("No songs found for the given text.")
                return None
        except Exception as e:
            print(f"Error performing full-text search: {e}")
            return None
        
    def _get_song_result(self, result):
        """
        Extract the song result from the search result.
        """
        formated_result = {
            "id": result["id"],
            "name": result["name"],
            "artists": ", ".join(artist["name"] for artist in result["artists"]),
            "album": result["album"]["name"],
            "uri": result["uri"],
            "url": f"https://open.spotify.com/track/{result['id']}"
        }
        return formated_result

    def add_song_to_song_queue(self, song_id: str):
        """
        Add a song to the Spotify song queue.
        """
        try:
            print(f"Adding song with ID {song_id} to the queue.")
            self.spotify_client.sp.add_to_queue(song_id)
            print("Song added to the queue successfully.")
        except Exception as e:
            print(f"Error adding song to the queue: {e}")
