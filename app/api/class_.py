from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..auth.dependencies import check_role
from ..database.engine import get_db
from ..models import Class
from ..schemas.class_ import ClassCreateRequest, ClassCreateResponse, DeleteClassResponse, ClassResponse
from ..services.class_service import ClassService

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("/", response_model=ClassCreateResponse)
async def create(
        user_data: ClassCreateRequest,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ClassService(db)
        message = service.create_class(user_data)

        return ClassCreateResponse(message=message)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.delete("/{id}", response_model=DeleteClassResponse)
async def delete(
        _id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        service = ClassService(db)
        message = service.delete_class(_id)

        return DeleteClassResponse(message=message)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.get("/get_all", response_model=List[ClassResponse])
async def get_all(
        db: Session = Depends(get_db),
        current_user=Depends(check_role("admin", ))
):
    try:
        classes = db.query(Class).all()
        return [
            ClassResponse(
                id=c.id,
                name=c.name,
                academic_year=c.academic_year

            )
            for c in classes
        ]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
