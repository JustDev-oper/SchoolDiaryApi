from typing import Optional

from sqlalchemy.orm import Session

from app.models import Role


def get_role_id_by_name(db: Session, name: str) -> Optional[int]:
    result = db.query(Role.id).filter(Role.name == name).first()
    return result[0] if result else None
