import logging
import twitchio
from twitchio.ext import commands
from backend.modules.spotify.services.song_request_service import SongRequestService

class RewardCommandsComponent(commands.Component):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.song_request_service = SongRequestService(bot.app)
        
        self.number_emojis = [
            "0\uFE0F\u20E3",
            "1\uFE0F\u20E3",
            "2\uFE0F\u20E3",
            "3\uFE0F\u20E3",
            "4\uFE0F\u20E3",
            "5\uFE0F\u20E3",
            "6\uFE0F\u20E3",
            "7\uFE0F\u20E3",
            "8\uFE0F\u20E3",
            "9\uFE0F\u20E3"
        ]
        logging.info("RewardCommandsComponent initialized.")

    # We use a listener in our Component to display the messages received.
    #@commands.Component.listener()
    #async def event_message(self, payload: twitchio.ChatMessage) -> None:
    #    print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

    @commands.command(name="songqueue", aliases=["sq"])
    async def songqueue(self, ctx: commands.Context) -> None:
        song_queue = self.song_request_service.get_song_queue()
        logging.info(f"Current song queue: {song_queue}")
        if not song_queue:
            await ctx.send("The song queue is empty.")
            return
        formatted_songs = self.format_numbered_list(
            [f"{song['artists']} - {song['name']}" for song in song_queue]
        )
        chunks = self.split_into_chunks(formatted_songs)
        for chunk in chunks:
            await ctx.send(chunk)
        
    @commands.command(name="lastsongs", aliases=["ls"])
    async def lastsongs(self, ctx: commands.Context) -> None:
        last_songs = self.song_request_service.get_last_songs()
        logging.info(f"Last songs played: {last_songs}")
        if not last_songs:
            await ctx.send("No songs have been played yet.")
            return
        formatted_songs = self.format_numbered_list(
            [f"{song['artists']} - {song['name']}" for song in last_songs]
        )
        chunks = self.split_into_chunks(formatted_songs)
        for chunk in chunks:
            await ctx.send(chunk)
        
    @commands.command(name="currentsong", aliases=["cs"])
    async def currentsong(self, ctx: commands.Context) -> None:
        current_song = self.song_request_service.get_current_song()
        logging.info(f"Current song: {current_song}")
        if not current_song:
            await ctx.send("No song is currently playing.")
            return
        formatted_song = f"🎵 Now Playing: {current_song['artists']} - {current_song['name']}"
        await ctx.send(formatted_song)
        
    @commands.command(name="findsong", aliases=["searchsong", "fs"])
    async def findsong(self, ctx: commands.Context, *, song_name: str) -> None:
        # todo: search for a song
        return
        
    @commands.command(name="skip")
    @commands.is_moderator()
    async def skip(self, ctx: commands.Context) -> None:
        self.song_request_service.skip_song()
        await ctx.send("⏭ Song skipped.")
    
    def format_numbered_list(self, items: list[str]) -> list[str]:
        """
        Formats a list of items with number emojis as prefixes
        """
        def get_number_emoji(number: int) -> str:
            # Converts a number to its corresponding emoji representation.
            return ''.join(self.number_emojis[int(digit)] for digit in str(number))

        formatted_list = [
            f"{get_number_emoji(i)} {item}" for i, item in enumerate(items, start=1)
        ]
        return formatted_list
    
    def split_into_chunks(self, items: list[str], max_chars: int = 399) -> list[str]:
        """
        Splits a list of strings into chunks where each chunk's total character count
        does not exceed the specified limit.
        """
        chunks = []
        current_chunk = ""

        for item in items:
            if len(current_chunk) + len(item) + 1 > max_chars:  # +1 for newline or space
                chunks.append(current_chunk.strip())
                current_chunk = item
            else:
                current_chunk += f"{item}\n"

        if current_chunk:  # Add the last chunk if it exists
            chunks.append(current_chunk.strip())

        return chunks
        
# This is our entry point for the module.
async def setup(bot: commands.Bot) -> None:
    await bot.add_component(RewardCommandsComponent(bot))
    