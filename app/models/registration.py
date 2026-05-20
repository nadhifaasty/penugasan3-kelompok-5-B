from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Registration(Base):
    __tablename__ = "registrations"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id   = Column(Integer, ForeignKey("events.id"), nullable=False)
    nama       = Column(String(255), nullable=True)
    nim        = Column(String(50), nullable=True)
    email      = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user  = relationship("User",  back_populates="registrations")
    event = relationship("Event", back_populates="registrations")