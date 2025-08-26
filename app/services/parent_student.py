from typing import Tuple, List

from sqlalchemy.orm import Session

from app.crud.parent_student import get_parents, get_students, get_students_from_parent
from app.crud.role import get_role_name_by_id
from app.crud.user import get_user_by_id
from app.models import User
from app.models.parent_student import ParentStudent
from app.schemas.parent_student import ParentConnectRequest


class ParentStudentService:
    def __init__(self, db: Session):
        self.db = db

    def is_parent(self, parent_id: int) -> Tuple[bool, str]:
        parent_user = get_user_by_id(self.db, parent_id)
        if parent_user is None:
            return False, f"Пользователь(Родитель) с id: {parent_id} не найден"

        parent_role = get_role_name_by_id(self.db, parent_user.role_id)
        if parent_role != "parent":
            return False, "Пользователь не является Родителем"

        return True, "Данные валидны"

    def is_student(self, student_id: int) -> Tuple[bool, str]:

        student_user = get_user_by_id(self.db, student_id)
        if student_user is None:
            return False, f"Пользователь(Ученик) с id: {student_id} не найден"

        student_role = get_role_name_by_id(self.db, student_user.role_id)
        if student_role != "student":
            return False, "Пользователь не является Учащимся"

        return True, "Данные валидны"

    def get_parents(self) -> List[User]:
        return get_parents(self.db)

    def get_students(self) -> List[User]:
        return get_students(self.db)

    def is_connected(self, parent_id: int, student_id: int) -> tuple[bool, str]:
        is_valid, message = self.is_parent(parent_id)
        if not is_valid:
            return is_valid, message

        is_valid, message = self.is_student(student_id)
        if not is_valid:
            return is_valid, message

        connection = (
            self.db.query(ParentStudent)
            .filter_by(parent_id=parent_id, student_id=student_id)
            .first()
        )

        if not connection:
            return False, "Связь родитель–ученик не найдена"

        return True, "Связь родитель–ученик найдена"

    def create_connection_with_parent(self, parent_id: int, student_id: int, user_data: ParentConnectRequest) -> Tuple[
        str, str, str]:
        is_valid, message = self.is_parent(parent_id)
        if not is_valid:
            raise ValueError(message)

        is_valid, message = self.is_student(student_id)
        if not is_valid:
            raise ValueError(message)

        new_connect = ParentStudent(
            parent_id=parent_id,
            student_id=student_id,
            relationship=user_data.relationship,
        )

        self.db.add(new_connect)
        self.db.commit()
        self.db.refresh(new_connect)

        parent_user = get_user_by_id(self.db, parent_id)
        student_user = get_user_by_id(self.db, student_id)
        parent = f"{parent_user.last_name} {parent_user.first_name} {parent_user.middle_name}"
        student = f"{student_user.last_name} {student_user.first_name} {student_user.middle_name}"

        return "Связь успешно создана", parent, student

    def delete_connection_with_parent(self, parent_id: int, student_id: int) -> str:
        is_valid, message = self.is_parent(parent_id)
        if not is_valid:
            return message

        is_valid, message = self.is_student(student_id)
        if not is_valid:
            return message

        # Находим запись
        is_connected, message = self.is_connected(parent_id, student_id)

        if not is_connected:
            raise ValueError(message)

        # Удаляем
        self.db.query(ParentStudent).filter_by(
            parent_id=parent_id,
            student_id=student_id
        ).delete()
        self.db.commit()

        return "Связь успешно удалена"

    def get_students_from_parent(self, parent_id: int) ->  Tuple[str, List[User]]:
        is_valid, message = self.is_parent(parent_id)
        if not is_valid:
            raise ValueError(message)

        return "Успешный запрос", get_students_from_parent(self.db, parent_id)
