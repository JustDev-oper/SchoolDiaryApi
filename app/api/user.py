from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.dependencies import check_role
from ..database.engine import get_db
from ..models import User
from ..schemas.user import UserCreateRequest, UserCreateResponse, UserResponse
from ..services.parent_student import ParentStudentService
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserCreateResponse)
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


@router.get("/parents")
def all_parents(
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ParentStudentService(db)
        parents = service.get_parents()

        return parents

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.get("/students")
def all_students(
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ParentStudentService(db)
        students = service.get_students()

        return students
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.get("/", response_model=List[UserResponse])
def all_users(
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        users = db.query(User).all()
        return [
            UserResponse(
                id=u.id,
                phone=u.phone,
                first_name=u.first_name,
                last_name=u.last_name,
                middle_name=u.middle_name,
                role=u.role.name,  # тут берем только имя роли
                login=u.login,
                date_of_birth=u.date_of_birth,
                class_id=u.class_id,
            )
            for u in users
        ]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.get("/{_id}", response_model=UserResponse)
def get_user(
        _id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        user = db.query(User).filter(User.id == _id).first()
        return UserResponse(
            id=user.id,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            role=user.role.name,
            login=user.login,
            date_of_birth=user.date_of_birth,
            class_id=user.class_id,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.put("/{id}", response_model=UserResponse)
def update_user(
        _id: int,
        user_data: UserCreateRequest,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = UserService(db)

        # TODO: дописать обновление данных пользователя

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
