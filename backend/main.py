import logging
import uvicorn
from backend.modules.logging.filters.sensitive_data_filter import SensitiveDataFilter

from backend.modules.twitch.twitch_bot_client import TwitchBotClient

# Apply log filtering
print("Applying sensitive data filter")
logging.getLogger("uvicorn.access").addFilter(SensitiveDataFilter())
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

if __name__ == "__main__":
    uvicorn.run("backend.modules.routing:app", host="127.0.0.1", port=8135, reload=True)
