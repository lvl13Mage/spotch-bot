from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

class SPAStaticFiles(StaticFiles):
    """Custom StaticFiles class to serve index.html for unmatched routes."""
    async def get_response(self, path: str, scope):
        # Log the requested path
        print("Path: ", path)

        # Resolve the full path to the requested file
        full_path = Path(self.directory) / path

        # If the path is empty, ".", or does not correspond to a file, serve index.html
        if path in ("", ".") or not full_path.is_file():
            index_path = Path(self.directory) / "index.html"
            print("Serving index.html for path: ", path)
            return FileResponse(index_path)

        # Otherwise, try to serve the requested file
        response = await super().get_response(path, scope)

        # If the file is not found, serve index.html
        if response.status_code == 404:
            index_path = Path(self.directory) / "index.html"
            print("Serving index.html for 404 path: ", path)
            return FileResponse(index_path)

        return response