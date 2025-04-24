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
# Assuming your static frontend files are in a folder named "frontend/dist"
frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "dist")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve index.html for the /static/ route
@app.get("/static", include_in_schema=False)
async def serve_static_index():
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)

# --- Uvicorn Config ---
def main():
    print("🚀 Starting Spotify-Twitch Bot API...")
    
    # Open the browser to the frontend
    webbrowser.open("http://127.0.0.1:8135/static")
    logging.info("If you don't see the browser, please open it manually at http://127.0.0.1:8135/static/")
    
    uvicorn.run(
        "backend.modules.routing:app",
        host="127.0.0.1",
        port=8135,
        reload=True,  # Set to False in prod
        log_level="info",
    )

if __name__ == "__main__":
    main()