from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from .utils import decode_token
from ..crud.user import get_user_by_id
from sqlalchemy.orm import Session
from ..database.engine import get_db

# Оставляем для обратной совместимости
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не найден токен аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if token.startswith("Bearer "):
        token = token[7:]  # Удаляем префикс "Bearer "
    return token


async def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
):
    token = get_token_from_cookie(request)
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректные данные токена",
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return user


# Проверка роли пользователя
def check_role(*allowed_roles: str):
    async def role_checker(user=Depends(get_current_user)):
        if user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения операции"
            )
        return user

    return role_checker
