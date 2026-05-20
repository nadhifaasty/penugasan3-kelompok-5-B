from sqlalchemy.orm import Session
from app.models.registration import Registration
from app.schemas.registration import RegistrationCreate, RegistrationUpdate

class RegistrationRepository:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Registration).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(Registration).filter(
            Registration.id == id
        ).first()

    def get_by_user_id(self, db: Session, user_id: int):
        return db.query(Registration).filter(
            Registration.user_id == user_id
        ).all()

    def get_by_event_id(self, db: Session, event_id: int):
        return db.query(Registration).filter(
            Registration.event_id == event_id
        ).all()

    def get_by_user_and_event(self, db: Session, user_id: int, event_id: int):
        return db.query(Registration).filter(
            Registration.user_id  == user_id,
            Registration.event_id == event_id
        ).first()

    def create(self, db: Session, data: RegistrationCreate):
        reg = Registration(**data.model_dump())
        db.add(reg)
        db.commit()
        db.refresh(reg)
        return reg

    def update(self, db: Session, id: int, data: RegistrationUpdate):
        reg = self.get_by_id(db, id)
        if not reg:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(reg, key, val)
        db.commit()
        db.refresh(reg)
        return reg

    def delete(self, db: Session, id: int):
        reg = self.get_by_id(db, id)
        if not reg:
            return None
        db.delete(reg)
        db.commit()
        return reg