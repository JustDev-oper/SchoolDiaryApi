from sqlalchemy.orm import Session

from app.models import Class


def get_class_by_id(id_: int, db: Session):
    return db.query(Class).filter(Class.id == id_).first()


def get_class_by_name(name: str, db: Session):
    return db.query(Class).filter(Class.name == name).first()
