import logging

class TwitchChatService:
    def __init__(self, bot):  # Use a string for the type hint
        self.bot = bot

    async def send_message(self, message: str):
        logging.info(f"Sending message: {message}")
        #await self.bot.wait_until_ready()  # Ensure bot is connected
        logging.info("Bot is ready to send messages.")
        user = self.bot.user  # Get the authenticated user
        if not user:
            logging.error("Bot user is not authenticated.")
            raise RuntimeError("Could not fetch target Twitch user")
        try: 
            await user.send_message(sender=user, message=message)
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise