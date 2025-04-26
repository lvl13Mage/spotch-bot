# 🛠️ Development Installation Guide

Follow these steps to set up the Spotify-Twitch Bot for development.

---

## Prerequisites

- **Python** (v3.9 or higher)
- **Node.js** (v16 or higher)
- **Docker** (optional, for database setup)

---

## 🚀 Installation Steps

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB/spotify-twitch-bot.git
cd spotify-twitch-bot
```

---

### 2️⃣ Set Up the Backend

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - If using Docker:
     ```bash
     docker-compose up -d
     ```
   - Otherwise, configure your database in `backend/modules/database/database.py`.

4. **Run the Backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```

---

### 3️⃣ Set Up the Frontend

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Run the Frontend**:
   ```bash
   npm run dev
   ```

---

## 🎯 Access the Application

- **Backend**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Frontend**: [http://localhost:5173](http://localhost:5173)

---

## 🧪 Running Tests

To run unit tests for the backend:

```bash
pytest
```

---

## 📜 License

This project is licensed under the **MIT License**.

---