from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The user's query or prompt")
    history: Optional[List[ChatMessage]] = Field(default=[], description="Previous conversation turns")

class ChatResponse(BaseModel):
    response: str
    tool_executed: Optional[str] = None
    tool_arguments: Optional[Dict[str, Any]] = None
    tool_status: Optional[str] = None
    provider: str
