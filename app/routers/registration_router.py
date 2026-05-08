from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.controllers.registration_controller import RegistrationController
from app.schemas.registration import RegistrationCreate, RegistrationUpdate, RegistrationResponse
from app.dependencies.auth import get_current_user

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
    current_user: dict = Depends(get_current_user)  # User must be authenticated
):
    return controller.create(db, data)

@router.patch("/{id}", response_model=RegistrationResponse)
def partial_update(id: int, data: RegistrationUpdate, db: Session = Depends(get_db)):
    return controller.update(db, id, data)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return controller.delete(db, id)