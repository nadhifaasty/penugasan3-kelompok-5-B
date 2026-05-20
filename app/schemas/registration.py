from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegistrationCreate(BaseModel):
    user_id:  int
    event_id: int

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "event_id": 2
            }
        }

class RegistrationUpdate(BaseModel):
    user_id:  Optional[int] = None
    event_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "event_id": 3
            }
        }

class RegistrationResponse(BaseModel):
    id:         int
    user_id:    int
    event_id:   int
    nama:       Optional[str] = None
    nim:        Optional[str] = None
    email:      Optional[str] = None
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class FrontendRegistrationCreate(BaseModel):
    eventId: int
    nama:    str
    nim:     str
    email:   str

    class Config:
        schema_extra = {
            "example": {
                "eventId": 1,
                "nama": "John Doe",
                "nim": "12345678",
                "email": "john@example.com"
            }
        }

class FrontendRegistrationResponse(BaseModel):
    message: str