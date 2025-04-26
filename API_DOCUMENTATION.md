# 📚 API Documentation

This document provides an overview of the API routes available in the Spotify-Twitch Bot.

---

## 🎁 Rewards API

| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| `GET`  | `/twitch/rewards`         | List all rewards.                       |
| `POST` | `/twitch/rewards`         | Create a new reward.                    |
| `PATCH`| `/twitch/rewards/{id}`    | Edit an existing reward.                |
| `DELETE`| `/twitch/rewards/{id}`   | Delete a reward (deactivate and sync).  |
| `POST` | `/twitch/rewards/sync`    | Sync rewards with Twitch.               |
| `GET`  | `/twitch/rewards/types`   | Fetch all reward types.                 |

---

## 🔑 Authentication API

### Twitch
| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| `GET`  | `/auth/twitch`            | Start Twitch OAuth.                     |
| `GET`  | `/auth/twitch/callback`   | Handle Twitch OAuth callback.           |
| `GET`  | `/auth/twitch/refresh-token` | Refresh Twitch token.                |

### Spotify
| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| `GET`  | `/auth/spotify/authorize` | Start Spotify OAuth.                    |
| `GET`  | `/auth/spotify/callback`  | Handle Spotify OAuth callback.          |

---

## ⚙️ Credentials API

| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| `POST` | `/credentials/twitch/set` | Set Twitch credentials.                 |
| `POST` | `/credentials/spotify/set`| Set Spotify credentials.                |
| `GET`  | `/credentials/twitch`     | Get Twitch credentials.                 |
| `GET`  | `/credentials/spotify`    | Get Spotify credentials.                |
| `DELETE`| `/credentials/twitch/delete` | Delete Twitch credentials.          |
| `DELETE`| `/credentials/spotify/delete`| Delete Spotify credentials.          |

---
