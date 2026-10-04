from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., description="Student register number or admin username")
    password: Optional[str] = Field(default="123456", description="User password (defaults to 123456 for students)")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    full_name: str
    register_number: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    register_number: Optional[int] = None
    full_name: str
    email: Optional[str] = None

    class Config:
        from_attributes = True
