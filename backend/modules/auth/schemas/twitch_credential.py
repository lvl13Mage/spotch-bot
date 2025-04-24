from pydantic import BaseModel
from typing import Optional

class TwitchCredentialInput(BaseModel):
    client_id: str
    client_secret: str
    scope: Optional[str] = None  # Optional, default to None
    redirect_uri: Optional[str] = None  # Optional, default to http://localhost:8000/auth/{service}/callback
    
