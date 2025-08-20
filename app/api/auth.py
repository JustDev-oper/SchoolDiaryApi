from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..auth.schemas import Token, LoginRequest
from ..database.engine import get_db
from ..services.user_service import UserService
from ..config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login(
        response: Response,
        login_data: LoginRequest,
        db: Session = Depends(get_db)
):
    user_service = UserService(db)
    success, result = user_service.authenticate_user(login_data.login, login_data.password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Устанавливаем secure httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {result}",
        httponly=True,
        secure=True,  # Только для HTTPS
        samesite="lax",  # Защита от CSRF
        expires=int((datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
        path="/"  # Cookie доступен для всех путей
    )

    return {"status": "success", "message": "Successfully authenticated"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    return {"status": "success", "message": "Successfully logged out"}
