from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TWITCH_CLIENT_ID: str
    TWITCH_CLIENT_SECRET: str
    TWITCH_REDIRECT_URI: str
    TWITCH_SCOPE: str

    class Config:
        env_file = ".env"

settings = Settings()
