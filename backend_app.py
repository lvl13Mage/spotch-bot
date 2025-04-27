import logging
import sys
import os
import uvicorn
import webbrowser
from backend.modules.logging.logging_config import setup_logging
from backend.modules.routing import app  # Import the FastAPI app from your routing module

# --- Ensure project root is in PYTHONPATH ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- Logging Setup ---
setup_logging()
logging.info("🛡️  Logging initialized with sensitive data filtering.")

# --- Mount Static Files ---
# Determine the path to the frontend/dist folder
if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller executable
    os.environ["APP_ENV"] = "production"  # Force production mode for PyInstaller builds
    os.chdir(os.path.dirname(sys.executable))  # Set working directory to the .exe location
    
# --- Uvicorn Config ---
def main():
    # Detect environment (default to development)
    app_env = os.getenv("APP_ENV", "production").lower()
    is_production = app_env == "production"

    logging.info(f"🚀 Starting Spotify-Twitch Bot API in {'production' if is_production else 'development'} mode...")
    
    webbrowser.open("http://127.0.0.1:8135/static")

    uvicorn.run(
        "backend.modules.routing:app",
        host="127.0.0.1",
        port=8135,
        reload=not is_production,  # Disable reload in production
        log_level="info",
    )

if __name__ == "__main__":
    main()