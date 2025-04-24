# 🎵 Twitch Spotify Bot

A local web application that integrates **Twitch** and **Spotify** for handling **song requests** and **persistent data storage**.

- **Backend**: FastAPI (Python) with SQLite and SQLAlchemy.
- **Frontend**: React with Vite, styled using TailwindCSS.
- **Runs Locally**: Configurable via a web dashboard.
- **Authentication**: Uses Twitch and Spotify OAuth.
- **Integration**: Supports StreamerBot and external REST/WebSocket APIs.
- **Data Storage**: SQLite for persistent settings and logs.

---

## 🚀 Features
✅ Song request management  
✅ Twitch & Spotify OAuth authentication  
✅ Web-based configuration dashboard  
✅ Persistent data storage using SQLite  
✅ REST API for external integration  
✅ Optional WebSocket support  

---

## 📦 Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB/twitch-spotify-bot.git
cd twitch-spotify-bot
```

### 2️⃣ Set Up a Virtual Environment
```sh
python -m venv venv
```

### 3️⃣ Activate the Virtual Environment
- **Windows (CMD or PowerShell)**
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux**
  ```sh
  source venv/bin/activate
  ```

### 4️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

---

## 🛠 Configuration
Create a `.env` file in the project root with your Twitch and Spotify credentials:

```env
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_CLIENT_SECRET=your_twitch_client_secret
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

---

## 🚀 Running the Application

### **Start the FastAPI Backend**
```sh
uvicorn backend.main:app --reload
```
The API will be available at:  
🔗 **http://127.0.0.1:8000**

### **Start the Frontend (React + Vite)**
```sh
cd frontend
npm install
npm run dev
```
The UI will be available at:  
🔗 **http://localhost:5173**

---

## 🎯 API Endpoints

| Method | Endpoint             | Description |
|--------|----------------------|-------------|
| GET    | `/auth/twitch`       | Start Twitch OAuth |
| GET    | `/auth/spotify`      | Start Spotify OAuth |
| POST   | `/songs`             | Add a song request |
| GET    | `/songs`             | Retrieve all song requests |
| GET    | `/settings`          | Fetch bot settings |
| GET    | `/logs`              | Retrieve logs |

For full API documentation, visit:  
🔗 **http://127.0.0.1:8000/docs**

---

## 🧪 Running Tests
To run unit tests, use:

```sh
pytest
```

---

## ⏹️ Stopping & Deactivating
To stop the backend, press **CTRL + C** in the terminal.  
To exit the virtual environment, run:

```sh
deactivate
```

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🌟 Contributing
Pull requests are welcome! Please open an issue first for discussion.

---

## 🎤 Contact
For questions or support, reach out via Twitch or Discord.

---

**Happy Streaming! 🚀🎶**
```