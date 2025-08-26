from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models import User, Role, ParentStudent


def get_parents(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(User)
        .join(Role, User.role_id == Role.id)  # явный join через role_id
        .options(joinedload(User.role))  # чтобы FastAPI смог сериализовать role
        .filter(Role.name == "parent")
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(User)
        .join(Role, User.role_id == Role.id)  # явный join через role_id
        .options(joinedload(User.role))  # чтобы FastAPI смог сериализовать role
        .filter(Role.name == "student")
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_students_from_parent(db: Session, parent_id: int, skip: int = 0, limit: int = 100) -> List[User]:
    return (
        db.query(User)
        .join(ParentStudent, ParentStudent.student_id == User.id)
        .filter(ParentStudent.parent_id == parent_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
