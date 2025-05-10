from backend.modules.spotify.spotify_client import SpotifyClient
from backend.modules.database.database import get_db_sync
import re
import logging

class SongRequestService:
    def __init__(self, app):
        self.db = get_db_sync()
        self.spotify_client = SpotifyClient(self.db, app)

    def search_song(self, query: str, items: int = 1):
        """
        Search for a song on Spotify.
        Differentiates between Spotify URI, Spotify URL, and full-text search.
        """

        # Check if the query is a Spotify URI
        if re.match(r"^spotify:track:[a-zA-Z0-9]+$", query):
            logging.info(f"Query is a Spotify URI: {query}")
            return self._get_song_by_uri(query)

        # Check if the query is a Spotify URL
        elif re.match(r"^https?://open\.spotify\.com(/[\w-]+)?/track/[a-zA-Z0-9]+", query):
            logging.info(f"Query is a Spotify URL: {query}")
            return self._get_song_by_url(query)

        # Otherwise, perform a full-text search
        else:
            logging.info(f"Query is a full-text search: {query}")
            return self._search_song_by_text(query, items)

    def _get_song_by_uri(self, uri: str):
        """Retrieve a song by its Spotify URI."""
        try:
            track_id = uri.split(":")[-1]
            track = self.spotify_client.sp.track(track_id)
            return [self._get_song_result(track)]
        except Exception as e:
            logging.error(f"Error retrieving song by URI: {e}")
            return None

    def _get_song_by_url(self, url: str):
        """Retrieve a song by its Spotify URL."""
        try:
            track_id = url.split("/")[-1].split("?")[0]
            track = self.spotify_client.sp.track(track_id)
            return [self._get_song_result(track)]
        except Exception as e:
            logging.error(f"Error retrieving song by URL: {e}")
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
                logging.info("No songs found for the given text.")
                return None
        except Exception as e:
            logging.error(f"Error performing full-text search: {e}")
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
            self.spotify_client.sp.add_to_queue(song_id)
            logging.info(f"Song added to the queue: {song_id}")
        except Exception as e:
            logging.error(f"Error adding song to the queue: {e}")

    def skip_song(self):
        """
        Skip the current song in the Spotify queue.
        """
        try:
            self.spotify_client.sp.next_track()
            logging.info("Song skipped successfully.")
        except Exception as e:
            logging.error(f"Error skipping song: {e}")
            
    def get_current_song(self):
        """
        Get the current song playing on Spotify.
        """
        try:
            current_playback = self.spotify_client.sp.current_playback()
            if current_playback and current_playback['is_playing']:
                current_track = current_playback['item']
                return self._get_song_result(current_track)
            else:
                logging.info("No song is currently playing.")
                return None
        except Exception as e:
            logging.error(f"Error getting current song: {e}")
            return None
        
    def get_song_queue(self, limit: int = 10):
        """
        Get the current song queue from Spotify as a list of Artist - SongName pairs.
        Return a list of dictionaries with song details.
        """
        try:
            logging.info("Getting the song queue.")
            current_playback = self.spotify_client.sp.queue()
            if current_playback and current_playback['queue']:
                queue = current_playback['queue'][:limit]
                return [self._get_song_result(track) for track in queue]
            else:
                logging.info("No song queue available.")
                return None
        except Exception as e:
            logging.error(f"Error getting song queue: {e}")
            return None
        
    def get_last_songs(self, limit: int = 10):
        """
        Get the last songs played on Spotify.
        """
        try:
            logging.info("Getting the last songs played.")
            current_playback = self.spotify_client.sp.current_user_recently_played()
            if current_playback and current_playback['items']:
                last_songs = current_playback['items'][:limit]
                return [self._get_song_result(item['track']) for item in last_songs]
            else:
                logging.info("No recently played songs available.")
                return None
        except Exception as e:
            logging.error(f"Error getting last songs: {e}")
            return None
    
    def find_song(self, song_name: str, items: int = 10):
        """
        Find a song by its name.
        """
        try:
            logging.info(f"Finding song: {song_name}")
            results = self._search_song_by_text(song_name, items)
            if results:
                return results
            else:
                logging.info("No songs found.")
                return None
        except Exception as e:
            logging.error(f"Error finding song: {e}")
            return None