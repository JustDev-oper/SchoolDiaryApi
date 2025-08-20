from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.user import User
from ..schemas.user import UserCreateRequest


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Получение пользователя по ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
    """Получение пользователя по номеру телефона"""
    return db.query(User).filter(User.phone == phone).first()


def get_user_by_login(db: Session, login: str) -> Optional[User]:
    """Получение пользователя по логину"""
    return db.query(User).filter(User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение списка пользователей с пагинацией"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: User) -> User:
    """Создание нового пользователя"""
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_data: dict) -> Optional[User]:
    """Обновление данных пользователя"""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Удаление пользователя"""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
