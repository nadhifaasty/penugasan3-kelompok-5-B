from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.registration_repository import RegistrationRepository
from app.schemas.registration import RegistrationCreate, RegistrationUpdate

# import untuk validasi keberadaan user & event
from app.models.user  import User
from app.models.event import Event

repo = RegistrationRepository()

class RegistrationService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return repo.get_all(db, skip, limit)

    def get_by_id(self, db: Session, id: int):
        reg = repo.get_by_id(db, id)
        if not reg:
            raise HTTPException(
                status_code=404,
                detail="Registration not found"
            )
        return reg

    def get_by_user_id(self, db: Session, user_id: int):
        # validasi user ada
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return repo.get_by_user_id(db, user_id)

    def get_by_event_id(self, db: Session, event_id: int):
        # validasi event ada
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )
        return repo.get_by_event_id(db, event_id)

    def create(self, db: Session, data: RegistrationCreate):
        # 1. validasi user ada
        user = db.query(User).filter(User.id == data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 2. validasi event ada
        event = db.query(Event).filter(Event.id == data.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # 3. cek kuota event
        current_registrations = len(
            repo.get_by_event_id(db, data.event_id)
        )
        if current_registrations >= event.quota:
            raise HTTPException(
                status_code=400,
                detail="Event is full, quota exceeded"
            )

        # 4. cek duplikat registrasi
        existing = repo.get_by_user_and_event(db, data.user_id, data.event_id)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="User already registered for this event"
            )

        return repo.create(db, data)

    def update(self, db: Session, id: int, data: RegistrationUpdate):
        # validasi registration ada
        reg = self.get_by_id(db, id)

        # jika user_id berubah, validasi user baru ada
        if data.user_id is not None and data.user_id != reg.user_id:
            user = db.query(User).filter(User.id == data.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

        # jika event_id berubah, validasi event baru ada dan kuota
        if data.event_id is not None and data.event_id != reg.event_id:
            event = db.query(Event).filter(Event.id == data.event_id).first()
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")

            # cek kuota event yang baru
            current_registrations = len(repo.get_by_event_id(db, data.event_id))
            if current_registrations >= event.quota:
                raise HTTPException(
                    status_code=400,
                    detail="Event is full, quota exceeded"
                )

            # cek duplikat registrasi
            existing = repo.get_by_user_and_event(db, reg.user_id, data.event_id)
            if existing and existing.id != id:
                raise HTTPException(
                    status_code=400,
                    detail="User already registered for this event"
                )

        return repo.update(db, id, data)

    def delete(self, db: Session, id: int):
        self.get_by_id(db, id)   # validasi ada dulu
        repo.delete(db, id)
        return {"message": "Registration cancelled successfully"}