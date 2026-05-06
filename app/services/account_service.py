from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AccountUpdate
from typing import Optional

repo = AccountRepository()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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