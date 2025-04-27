
class TwitchChatService:
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, message: str):
        await self.bot.wait_until_ready()  # Ensure bot is connected
        user = self.bot.user  # Get the authenticated user
        if not user:
            raise RuntimeError("Could not fetch target Twitch user")
        await user.send_message(sender=user, message=message)