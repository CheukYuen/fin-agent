from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str
    model: Optional[str] = "gpt-3.5-turbo"

class ChatResponse(BaseModel):
    reply: str
