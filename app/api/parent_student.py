from heapq import merge

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import check_role
from app.database.engine import get_db
from app.schemas.parent_student import ConnectParentResponse, ParentConnectRequest, DisconnectParentResponse, \
    GetParentStudentsResponse
from app.schemas.user import UserResponse
from app.services.parent_student import ParentStudentService

router = APIRouter(prefix="/parents", tags=["Parent & Students"])


@router.get("/{parent_id}/students/", response_model=GetParentStudentsResponse)
async def get_students_from_parent(
        parent_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", )),

):
    try:
        service = ParentStudentService(db)
        message, get_students = service.get_students_from_parent(parent_id)

        students = [
            UserResponse(
                id=student.id,
                phone=student.phone,
                first_name=student.first_name,
                last_name=student.last_name,
                middle_name=student.middle_name,
                role=student.role.name,
                login=student.login,
                date_of_birth=student.date_of_birth,
                class_id=student.class_id
            )
            for student in get_students
        ]

        return GetParentStudentsResponse(message=message, students=students)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.post("/{parent_id}/students/{student_id}", response_model=ConnectParentResponse)
async def connect_parent(
        parent_id: int, student_id: int,
        user_data: ParentConnectRequest,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ParentStudentService(db)
        message, parent, student = service.create_connection_with_parent(parent_id, student_id, user_data)

        return ConnectParentResponse(message=message, parent=parent, student=student)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.delete("/{parent_id}/students/{student_id}", response_model=DisconnectParentResponse)
def detach_parent(
        parent_id: int, student_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ParentStudentService(db)
        message = service.delete_connection_with_parent(parent_id, student_id)

        return DisconnectParentResponse(message=message)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


# TODO: реализовать ручку put (изменение связи)