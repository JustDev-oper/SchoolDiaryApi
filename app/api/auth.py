from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session

from ..auth.schemas import LoginRequest
from ..auth.utils import decode_token
from ..config import settings
from ..database.engine import get_db
from ..services.user_service import UserService

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
    success, token = user_service.authenticate_user(login_data.login, login_data.password, role=login_data.role)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=token,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ставим cookie **только с токеном**, без "Bearer "
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # True только на HTTPS
        samesite="lax",
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # в секундах
        path="/"
    )

    return {"status": "success", "message": "Successfully authenticated"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    return {"status": "success", "message": "Successfully logged out"}


@router.get("/check")
async def check(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return {"authenticated": False}

    payload = decode_token(token)
    if not payload:
        return {"authenticated": False}

    return {"authenticated": True}
