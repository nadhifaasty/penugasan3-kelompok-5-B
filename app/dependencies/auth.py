from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.role import Role
from typing import Optional

# tokenUrl cuma dipakai oleh Swagger untuk tombol "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency yang memvalidasi JWT Bearer Token.
    Inject ke endpoint manapun yang butuh autentikasi:
        current_user: dict = Depends(get_current_user)
    Returns: dict dengan keys: sub (username), user_id, role_id
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kadaluarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


def get_role_name(db: Session, role_id: int) -> Optional[str]:
    """Helper function to get role name from database"""
    role = db.query(Role).filter(Role.id == role_id).first()
    return role.name if role else None


def require_admin(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Dependency untuk restrict endpoint hanya untuk Admin.
    Inject ke endpoint yang hanya admin bisa akses:
        admin_user: dict = Depends(require_admin)
    """
    role_id = current_user.get("role_id")
    role_name = get_role_name(db, role_id)
    
    # Check if role name is "Admin" (case-insensitive)
    if role_name and role_name.lower() == "admin":
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Hanya Admin yang bisa mengakses endpoint ini"
    )


def require_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Dependency untuk restrict endpoint hanya untuk User biasa (bukan Admin).
    Inject ke endpoint yang hanya user bisa akses:
        user: dict = Depends(require_user)
    """
    role_id = current_user.get("role_id")
    role_name = get_role_name(db, role_id)
    
    # Check if role name is NOT "Admin"
    if role_name and role_name.lower() != "admin":
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User dengan role Admin tidak bisa mengakses endpoint ini"
    )


def get_role_id_from_token(current_user: dict = Depends(get_current_user)) -> int:
    """
    Helper untuk extract role_id dari current user.
    """
    return current_user.get("role_id")