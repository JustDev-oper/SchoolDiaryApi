from typing import Tuple

from sqlalchemy.orm import Session

from app.crud.class_ import get_class_by_name, get_class_by_id
from app.models import Class
from app.schemas.class_ import ClassCreateRequest


class ClassService:
    def __init__(self, db: Session):
        self.db = db

    def is_unique(self, user_data) -> Tuple[bool, str]:
        class_ = get_class_by_name(db=self.db, name=user_data.name)
        if class_ is not None:
            return False, f"Класс с названием {user_data.name} уже существует"
        return True, ""

    def is_unique_by_id(self, user_data) -> Tuple[bool, str]:
        class_ = get_class_by_id(db=self.db, id_=user_data.id)
        if class_ is not None:
            return False, f"Класс с названием: {user_data.name} уже существует"

        return True, ""

    def create_class(self, user_data: ClassCreateRequest) -> str:
        is_valid, message = self.is_unique(user_data)
        if not is_valid:
            raise ValueError(message)

        class_ = Class(name=user_data.name, academic_year=user_data.academic_year)

        self.db.add(class_)
        self.db.commit()
        self.db.refresh(class_)

        return "Успешно"

    def delete_class(self, _id: int) -> str:

        try:
            self.db.query(Class).filter_by(
                id=_id
            ).delete()
            self.db.commit()

        except Exception as e:
            raise ValueError(e)

        return "Успешно удалён класс"
