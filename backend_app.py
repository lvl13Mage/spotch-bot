import logging
import sys
import os
import uvicorn
import webbrowser
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.modules.logging.filters.sensitive_data_filter import SensitiveDataFilter
from backend.modules.routing import app  # Import the FastAPI app from your routing module

# --- Ensure project root is in PYTHONPATH ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- Logging Setup ---
print("🛡️  Applying sensitive data filter...")
logging.getLogger("uvicorn.access").addFilter(SensitiveDataFilter())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# --- Mount Static Files ---
# Determine the path to the frontend/dist folder
if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller executable
    frontend_path = os.path.join(sys._MEIPASS, "frontend", "dist")
    os.environ["APP_ENV"] = "production"  # Force production mode for PyInstaller builds
else:
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "dist")

# Mount the static files
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve index.html for the /static/ route
@app.get("/static", include_in_schema=False)
async def serve_static_index():
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)

# --- Uvicorn Config ---
def main():
    # Detect environment (default to development)
    app_env = os.getenv("APP_ENV", "development").lower()
    is_production = app_env == "production"

    print(f"🚀 Starting Spotify-Twitch Bot API in {'production' if is_production else 'development'} mode...")
    
    webbrowser.open("http://127.0.0.1:8135/static")
    logging.info("If you don't see the browser, please open it manually at http://127.0.0.1:8135/static/")

    uvicorn.run(
        "backend.modules.routing:app",
        host="127.0.0.1",
        port=8135,
        reload=not is_production,  # Disable reload in production
        log_level="info",
    )

if __name__ == "__main__":
    main()