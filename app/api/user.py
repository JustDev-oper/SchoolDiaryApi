from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.dependencies import check_role
from ..schemas.parent_student import ConnectParentResponse, ParentConnectRequest, DisconnectParentResponse, \
    DisconnectParentRequest
from ..schemas.user import UserCreateRequest, UserCreateResponse
from ..services.parent_student import ParentStudentService
from ..services.user_service import UserService
from ..database.engine import get_db

router = APIRouter()


@router.post("/users/create", response_model=UserCreateResponse)
def create_user(
        user_data: UserCreateRequest,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
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
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.post("/users/connect_parent", response_model=ConnectParentResponse)
async def connect_parent(
        user_data: ParentConnectRequest,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ParentStudentService(db)
        message, parent, student = service.create_connection_with_parent(user_data)

        return ConnectParentResponse(message=message, parent=parent, student=student)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.delete("/users/detach_parent", response_model=DisconnectParentResponse)
def detach_parent(
        user_data: DisconnectParentRequest,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ParentStudentService(db)
        message = service.delete_connection_with_parent(user_data)

        return DisconnectParentResponse(message=message)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
