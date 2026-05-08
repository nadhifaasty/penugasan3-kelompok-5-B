from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.controllers.event_controller import EventController
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.dependencies.auth import require_admin, get_current_user

router     = APIRouter(prefix="/events", tags=["Event"])
controller = EventController()

@router.get("/", response_model=List[EventResponse])
def get_all_events(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
):
    return controller.get_all(db, skip, limit, search)

@router.get("/upcoming", response_model=List[EventResponse])
def get_upcoming_events(db: Session = Depends(get_db)):
    return controller.get_upcoming(db)

@router.get("/{id}", response_model=EventResponse)
def get_event(id: int, db: Session = Depends(get_db)):
    return controller.get_by_id(db, id)

@router.post("/", response_model=EventResponse, status_code=201)
def create_event(
    data: EventCreate,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin)  # Only Admin
):
    return controller.create(db, data)

@router.patch("/{id}", response_model=EventResponse)
def update_event(
    id: int,
    data: EventUpdate,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin)  # Only Admin
):
    return controller.update(db, id, data)

@router.delete("/{id}")
def delete_event(
    id: int,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin)  # Only Admin
):
    return controller.delete(db, id)