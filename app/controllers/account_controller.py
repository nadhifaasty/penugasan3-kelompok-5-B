from sqlalchemy.orm import Session
from app.services.account_service import AccountService
from app.schemas.account import AccountCreate, AccountUpdate
from typing import Optional

service = AccountService()

class AccountController:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
        return service.get_all(db, skip, limit, search)

    def get_by_id(self, db: Session, id: int):
        return service.get_by_id(db, id)

    def get_by_user_id(self, db: Session, user_id: int):
        return service.get_by_user_id(db, user_id)

    def create(self, db: Session, data: AccountCreate):
        return service.create(db, data)

    def update(self, db: Session, id: int, data: AccountUpdate):
        return service.update(db, id, data)

    def delete(self, db: Session, id: int):
        return service.delete(db, id)
    
    def login(self, db: Session, username: str, password: str):
        return service.login(db, username, password)