from typing import Tuple, List

from sqlalchemy.orm import Session

from app.crud.parent_student import get_parents, get_students
from app.crud.role import get_role_name_by_id
from app.crud.user import get_user_by_id
from app.models import User
from app.models.parent_student import ParentStudent
from app.schemas.parent_student import ParentConnectRequest, DisconnectParentRequest


class ParentStudentService:
    def __init__(self, db: Session):
        self.db = db

    def is_parent_and_student(self, user_data) -> Tuple[bool, str]:
        parent_user = get_user_by_id(self.db, user_data.parent_id)
        if parent_user is None:
            return False, f"Пользователь(Родитель) с id: {user_data.parent_id} не найден"

        student_user = get_user_by_id(self.db, user_data.student_id)
        if student_user is None:
            return False, f"Пользователь(Ученик) с id: {user_data.parent_id} не найден"

        parent_role = get_role_name_by_id(self.db, parent_user.role_id)
        if parent_role != "parent":
            return False, "Пользователь не является Родителем"

        student_role = get_role_name_by_id(self.db, student_user.role_id)
        if student_role != "student":
            return False, "Пользователь не является Учащимся"

        return True, "Данные валидны"

    def get_parents(self) -> List[User]:
        return get_parents(self.db)

    def get_students(self) -> List[User]:
        return get_students(self.db)

    from typing import Tuple

    def is_connected(self, user_data) -> tuple[bool, str]:
        is_valid, message = self.is_parent_and_student(user_data)
        if not is_valid:
            return is_valid, message

        connection = (
            self.db.query(ParentStudent)
            .filter_by(parent_id=user_data.parent_id, student_id=user_data.student_id)
            .first()
        )

        if not connection:
            return False, "Связь родитель–ученик не найдена"

        return True, "Связь родитель–ученик найдена"

    def create_connection_with_parent(self, user_data: ParentConnectRequest) -> Tuple[str, str, str]:
        is_valid, message = self.is_parent_and_student(user_data)
        if not is_valid:
            raise ValueError(message)

        new_connect = ParentStudent(
            parent_id=user_data.parent_id,
            student_id=user_data.student_id,
            relationship=user_data.relationship,
        )

        self.db.add(new_connect)
        self.db.commit()
        self.db.refresh(new_connect)

        parent_user = get_user_by_id(self.db, user_data.parent_id)
        student_user = get_user_by_id(self.db, user_data.student_id)
        parent = f"{parent_user.last_name} {parent_user.first_name} {parent_user.middle_name}"
        student = f"{student_user.last_name} {student_user.first_name} {student_user.middle_name}"

        return "Связь успешно создана", parent, student

    def delete_connection_with_parent(self, user_data: DisconnectParentRequest) -> str:
        is_valid, message = self.is_parent_and_student(user_data)
        if not is_valid:
            raise ValueError(message)

        # Находим запись
        is_connected, message = self.is_connected(user_data)

        if not is_connected:
            raise ValueError(message)

        # Удаляем
        self.db.query(ParentStudent).filter_by(
            parent_id=user_data.parent_id,
            student_id=user_data.student_id
        ).delete()
        self.db.commit()

        return "Связь успешно удалена"
