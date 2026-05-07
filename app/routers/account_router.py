from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.controllers.account_controller import AccountController
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse, LoginRequest, TokenResponse
from app.dependencies.auth import get_current_user

router     = APIRouter(prefix="/accounts", tags=["Account"])
controller = AccountController()

# public endpoints

@router.post("/login", response_model=TokenResponse, summary="Login dan dapatkan JWT token")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return controller.login(db, data.username, data.password)

@router.post("/", response_model=AccountResponse, status_code=201, summary="Daftar akun baru")
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    return controller.create(db, data)

# protected endpoints (butuh bearer token)

@router.get("/", response_model=List[AccountResponse], dependencies=[Depends(get_current_user)])
def get_all_accounts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
):
    return controller.get_all(db, skip, limit, search)

@router.get("/user/{user_id}", response_model=List[AccountResponse], dependencies=[Depends(get_current_user)])
def get_accounts_by_user(user_id: int, db: Session = Depends(get_db)):
    return controller.get_by_user_id(db, user_id)

@router.get("/{id}", response_model=AccountResponse, dependencies=[Depends(get_current_user)])
def get_account(id: int, db: Session = Depends(get_db)):
    return controller.get_by_id(db, id)

@router.patch("/{id}", response_model=AccountResponse, dependencies=[Depends(get_current_user)])
def update_account(id: int, data: AccountUpdate, db: Session = Depends(get_db)):
    return controller.update(db, id, data)

@router.delete("/{id}", dependencies= [Depends(get_current_user)])
def delete_account(id: int, db: Session = Depends(get_db)):
    return controller.delete(db, id)