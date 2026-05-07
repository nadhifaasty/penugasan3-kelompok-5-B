from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import settings

# tokenUrl cuma dipakai oleh Swagger untuk tombol "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency yang memvalidasi JWT Bearer Token.
    Inject ke endpoint manapun yang butuh autentikasi:
        current_user: dict = Depends(get_current_user)
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