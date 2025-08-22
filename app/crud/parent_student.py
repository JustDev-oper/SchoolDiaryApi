from sqlalchemy.orm import Session, joinedload

from app.models import User, Role


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
