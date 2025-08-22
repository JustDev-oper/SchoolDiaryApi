import re
import random
import string
from typing import Tuple
from datetime import timedelta, timezone
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreateRequest
from ..crud.user import get_user_by_phone, get_user_by_login
from ..crud.role import get_role_id_by_name
from ..auth.utils import create_token
from ..config import settings
from passlib.context import CryptContext

# Создаем контекст для хеширования паролей
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Стандартное количество раундов
)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, login: str, password: str, role: str) -> Tuple[bool, str]:
        """Аутентификация пользователя"""
        user = get_user_by_login(self.db, login)
        if not user:
            return False, "Неверный логин или пароль"

        try:
            stored_hash = str(user.password_hash)
            try:
                password_check = pwd_context.verify(password, stored_hash)
            except Exception as ve:
                return False, "Ошибка проверки пароля"
            if not password_check:
                return False, "Неверный логин или пароль"
            if role != user.role.name:
                return False, "Неверный логин или пароль"
        except Exception as e:
            return False, "Ошибка проверки пароля"

        # Создаем данные для токена
        token_data = {
            "user_id": user.id,
            "role": user.role.name,
            "sub": user.login
        }

        # Создаем токен
        access_token = create_token(
            data=token_data,
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return True, access_token

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Проверка корректности номера телефона"""
        pattern = r'^\+7\d{10}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def generate_login(first_name: str, last_name: str) -> str:
        """Генерация логина на основе ФИО"""
        # Транслитерация имени и фамилии
        transliteration = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }

        # Преобразуем имя и фамилию в нижний регистр
        first_name = first_name.lower()
        last_name = last_name.lower()

        # Транслитерация
        trans_first_name = ''.join(transliteration.get(c, c) for c in first_name)
        trans_last_name = ''.join(transliteration.get(c, c) for c in last_name)

        # Генерация базового логина
        base_login = f"{trans_last_name}_{trans_first_name}"

        # Добавляем случайные цифры
        random_digits = ''.join(random.choices(string.digits, k=3))
        return f"{base_login}_{random_digits}"

    @staticmethod
    def generate_password(length: int = 10) -> str:
        """Генерация безопасного пароля"""
        # Определяем наборы символов
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*"

        # Убедимся, что пароль содержит как минимум по одному символу каждого типа
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]

        # Добавляем остальные символы
        all_characters = lowercase + uppercase + digits + special
        password.extend(random.choices(all_characters, k=length - 4))

        # Перемешиваем пароль
        random.shuffle(password)
        return ''.join(password)

    def validate_user_data(self, user_data: UserCreateRequest) -> Tuple[bool, str]:
        """Валидация данных пользователя"""
        # Проверка формата телефона
        if not self.validate_phone(user_data.phone):
            return False, "Неверный формат номера телефона"

        # Проверка существования пользователя с таким телефоном
        existing_user = get_user_by_phone(self.db, user_data.phone)
        if existing_user:
            return False, "Пользователь с таким номером телефона уже существует"

        # Проверка длины имени и фамилии
        if len(user_data.first_name) < 2 or len(user_data.last_name) < 2:
            return False, "Имя и фамилия должны содержать минимум 2 символа"

        return True, "Данные валидны"

    def create_user(self, user_data: UserCreateRequest) -> Tuple[str, str, str]:
        """Создание нового пользователя"""
        # Валидация данных
        is_valid, message = self.validate_user_data(user_data)
        if not is_valid:
            raise ValueError(message)

        # Генерация логина и пароля
        login = self.generate_login(user_data.first_name, user_data.last_name)

        # Проверяем уникальность логина
        while get_user_by_login(self.db, login):
            login = self.generate_login(user_data.first_name, user_data.last_name)

        # Генерируем пароль
        password = self.generate_password()

        # Хешируем пароль для хранения
        hashed_password = pwd_context.hash(password)

        # Создаем пользователя
        from datetime import datetime
        new_user = User(
            phone=user_data.phone,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            middle_name=user_data.middle_name,
            role_id=get_role_id_by_name(self.db, user_data.role),  # Получаем ID роли из базы данных
            login=login,
            password_hash=hashed_password,
            created_at=datetime.now(timezone.utc)
        )

        # Сохраняем в базу данных
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return "Пользователь успешно создан", login, password
