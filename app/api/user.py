from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from ..schemas.user import UserCreateRequest, UserCreateResponse
from ..services.user_service import UserService
from ..database.engine import get_db

router = APIRouter()


@router.post("/users/create", response_model=UserCreateResponse)
def create_user(
        user_data: UserCreateRequest,
        db: Session = Depends(get_db)
):
    """
    Создание нового пользователя (только для завуча)
    """
    try:
        service = UserService(db)
        message, login, password = service.create_user(user_data)

        return UserCreateResponse(
            message=message,
            login=login,
            password=password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error creating user: {str(e)}")  # Временное логирование для отладки
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
