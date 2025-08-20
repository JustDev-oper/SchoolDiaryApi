from pydantic import BaseModel, Field
from typing import Optional


class UserCreateRequest(BaseModel):
    phone: str = Field(..., description="Номер телефона пользователя")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    middle_name: Optional[str] = Field(None, description="Отчество пользователя")
    role: str = Field(..., description="Роль пользователя (head_teacher/teacher/student/parent)")

    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+79001234567",
                "first_name": "Иван",
                "last_name": "Иванов",
                "middle_name": "Иванович",
                "role": "teacher"
            }
        }


class UserCreateResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате операции")
    login: str = Field(..., description="Сгенерированный логин пользователя")
    password: str = Field(..., description="Сгенерированный пароль пользователя")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Пользователь успешно создан",
                "login": "ivanov_ivan_123",
                "password": "xK9#mP2$vL"
            }
        }


class UserResponse(BaseModel):
    id: int
    phone: str
    first_name: str
    last_name: str
    middle_name: Optional[str]
    role: str
    login: str

    class Config:
        from_attributes = True
