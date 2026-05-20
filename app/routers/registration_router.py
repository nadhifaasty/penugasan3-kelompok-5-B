from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.controllers.registration_controller import RegistrationController
from app.schemas.registration import RegistrationCreate, RegistrationUpdate, RegistrationResponse, FrontendRegistrationCreate, FrontendRegistrationResponse
from app.dependencies.auth import get_current_user
from app.models.event import Event
from app.models.registration import Registration
from datetime import datetime

router     = APIRouter(prefix="/registrations", tags=["Registration"])
controller = RegistrationController()

@router.get("/", response_model=List[RegistrationResponse])
def get_all(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return controller.get_all(db, skip, limit)

@router.get("/user/{user_id}", response_model=List[RegistrationResponse])
def get_by_user(user_id: int, db: Session = Depends(get_db)):
    return controller.get_by_user_id(db, user_id)

@router.get("/event/{event_id}", response_model=List[RegistrationResponse])
def get_by_event(event_id: int, db: Session = Depends(get_db)):
    return controller.get_by_event_id(db, event_id)

@router.get("/{id}", response_model=RegistrationResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return controller.get_by_id(db, id)

@router.post("/", response_model=RegistrationResponse, status_code=201)
def create(
    data: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return controller.create(db, data)

@router.post("/frontend", response_model=FrontendRegistrationResponse, status_code=201)
def create_frontend(
    data: FrontendRegistrationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")

    event = db.query(Event).filter(Event.id == data.eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event tidak ditemukan")

    existing = db.query(Registration).filter(
        Registration.user_id == user_id,
        Registration.event_id == data.eventId
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Anda sudah terdaftar di event ini")

    current_count = db.query(Registration).filter(
        Registration.event_id == data.eventId
    ).count()
    if current_count >= event.quota:
        raise HTTPException(status_code=400, detail="Kuota event sudah penuh")

    reg = Registration(
        user_id=user_id,
        event_id=data.eventId,
        nama=data.nama,
        nim=data.nim,
        email=data.email,
        created_at=datetime.utcnow()
    )
    db.add(reg)
    db.commit()
    db.refresh(reg)

    return FrontendRegistrationResponse(message="Registrasi berhasil!")

@router.patch("/{id}", response_model=RegistrationResponse)
def partial_update(id: int, data: RegistrationUpdate, db: Session = Depends(get_db)):
    return controller.update(db, id, data)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return controller.delete(db, id)