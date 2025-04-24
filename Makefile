# Variables
FRONTEND_DIR := frontend
BACKEND_APP := backend_app.py
DIST_DIR := $(FRONTEND_DIR)/dist
EXECUTABLE := dist/spotify-bot
PYINSTALLER_SPEC := spotify-bot.spec

# Default target
.PHONY: all
all: build

# example call: make migrate m="My Migration Name"
migrate:
	alembic -c backend/migrations/alembic.ini revision --autogenerate -m "$(m)"
upgrade:
	alembic -c backend/migrations/alembic.ini upgrade head

# Build the frontend
.PHONY: frontend
frontend:
    cd $(FRONTEND_DIR) && npm install && npm run build

# Package the backend into an executable
.PHONY: backend
backend: frontend
    pyinstaller --name spotify-bot --onefile $(BACKEND_APP)

# Clean up build artifacts
.PHONY: clean
clean:
    rm -rf $(DIST_DIR) $(EXECUTABLE) build __pycache__ *.spec

# Run the application (development mode)
.PHONY: run
run:
    python3 $(BACKEND_APP)

# Install Python dependencies
.PHONY: install
install:
    pip install -r requirements.txt

# Install development dependencies
.PHONY: install-dev
install-dev:
    pip install -r requirements-dev.txt

# Build everything (frontend + backend)
.PHONY: build
build: frontend backend

# Run the application from the built executable
.PHONY: run-executable
run-executable:
    ./$(EXECUTABLE)