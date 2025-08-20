from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from ..config import settings

config = settings


def create_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Декодирование и проверка JWT токена"""
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    except JWTError:
        return None
