from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.controllers.user_controller import UserController
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.dependencies.auth import get_current_user

router     = APIRouter(
    prefix="/users",
    tags=["User"],
    # dependencies=[Depends(get_current_user)],   # semua endpoint butuh token
)
controller = UserController()


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
):
    return controller.get_all(db, skip, limit, search)


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    return controller.get_by_id(db, id)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return controller.create(db, data)


@router.patch("/{id}", response_model=UserResponse)
def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return controller.update(db, id, data)


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return controller.delete(db, id)
