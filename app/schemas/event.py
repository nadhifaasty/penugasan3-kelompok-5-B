from pydantic import BaseModel, field_validator, field_serializer, model_validator, computed_field
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    name:        str
    description: Optional[str] = None
    quota:       int
    started_at:  datetime
    ended_at:    datetime

    @field_validator("quota")
    @classmethod
    def quota_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("quota must be greater than 0")
        return v

    @model_validator(mode="after")
    def ended_after_started(self):
        if self.ended_at <= self.started_at:
            raise ValueError("ended_at must be after started_at")
        return self

    class Config:
        schema_extra = {
            "example": {
                "name": "Workshop Python",
                "description": "Pelatihan dasar FastAPI",
                "quota": 50,
                "started_at": "2026-05-01T09:00:00",
                "ended_at": "2026-05-01T12:00:00"
            }
        }

class EventUpdate(BaseModel):
    name:        Optional[str]      = None
    description: Optional[str]      = None
    quota:       Optional[int]      = None
    started_at:  Optional[datetime] = None
    ended_at:    Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Workshop Python Lanjutan",
                "quota": 60
            }
        }

class EventResponse(BaseModel):
    id:          int
    name:        str
    description: Optional[str]
    quota:       int
    started_at:  datetime
    ended_at:    datetime
    created_at:  Optional[datetime]
    updated_at:  Optional[datetime]

    @computed_field
    @property
    def title(self) -> str:
        return self.name

    @computed_field
    @property
    def date(self) -> str:
        return self.started_at.strftime('%Y-%m-%d %H:%M') if isinstance(self.started_at, datetime) else str(self.started_at)

    @field_serializer('started_at')
    def serialize_started_at(self, value: datetime):
        return value.strftime('%Y-%m-%d %H:%M')

    @field_serializer('ended_at')
    def serialize_ended_at(self, value: datetime):
        return value.strftime('%Y-%m-%d %H:%M')

    class Config:
        from_attributes = True