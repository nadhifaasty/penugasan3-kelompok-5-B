from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AccountCreate(BaseModel):
    user_id: int
    role_id: int
    email: str
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "role_id": 2,
                "email": "user@example.com",
                "username": "user123",
                "password": "securepassword"
            }
        }

class AccountUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "email": "new.email@example.com",
                "username": "newuser",
                "password": "newsecurepassword"
            }
        }

class AccountResponse(BaseModel):
    id: int
    user_id: int
    role_id: int
    email: str
    username: str
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"