from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_magic_link_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.MAGIC_LINK_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire, "type": "magic_link"}
    encoded_jwt = jwt.encode(to_encode, settings.MAGIC_LINK_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_magic_link_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.MAGIC_LINK_SECRET, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if email is None or token_type != "magic_link":
            return None
        return email
    except JWTError:
        return None
