from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AccountUpdate
from app.config import settings
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt

repo = AccountRepository()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

class AccountService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
        return repo.get_all(db, skip, limit, search)

    def get_by_id(self, db: Session, id: int):
        account = repo.get_by_id(db, id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def get_by_user_id(self, db: Session, user_id: int):
        return repo.get_by_user_id(db, user_id)

    def create(self, db: Session, data: AccountCreate):
        existing = repo.get_by_username(db, data.username)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )
        data.password = hash_password(data.password)
        return repo.create(db, data)

    def update(self, db: Session, id: int, data: AccountUpdate):
        self.get_by_id(db, id)
        if data.password:
            data.password = hash_password(data.password)
        return repo.update(db, id, data)

    def delete(self, db: Session, id: int):
        self.get_by_id(db, id)
        repo.delete(db, id)
        return {"message": "Account deleted successfully"}
    
    def login(self, db: Session, username: str, password: str):
        account = repo.get_by_username(db, username)

        if not account or not verify_password(password, account.password):
            raise HTTPException(status_code=401, detail="Username atau password salah")

        token = create_access_token({
            "sub": account.username,
            "user_id": account.user_id,
            "role_id": account.role_id  # Include role_id di JWT
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }