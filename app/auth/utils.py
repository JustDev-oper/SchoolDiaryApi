from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from ..config import settings

config = settings


def create_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена с корректным временем истечения"""
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    # Преобразуем в timestamp
    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Декодирование и проверка JWT токена"""
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    except JWTError:
        return None
