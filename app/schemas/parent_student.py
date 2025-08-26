from typing import List

from pydantic import BaseModel, Field

from app.schemas.user import UserResponse


class ParentConnectRequest(BaseModel):
    relationship: str = Field(..., description="Кто он для учащегося")

    class Config:
        json_schema_extra = {
            "example": {
                "parent_id": "1",
                "student_id": "2",
                "relationship": "father",
            }
        }


class GetParentStudentsResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате операции")
    students: List[UserResponse] = Field(..., description="Список учеников родителя")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Успешный запрос",
                "students": [
                    {
                        "id": 1,
                        "phone": "+79001234567",
                        "first_name": "Иван",
                        "last_name": "Иванов",
                        "middle_name": "Иванович",
                        "role": "student",
                        "login": "ivanov_ivan_123",
                        "date_of_birth": "2010-05-01",
                        "class_id": 3
                    }
                ]
            }
        }


class ConnectParentResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате операции")
    parent: str = Field(..., description="Опекун учащегося")
    student: str = Field(..., description="Учащийся")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Связь успешно создана",
                "parent": "Иванов Иван Иванович",
                "student": "Иванов Вася Иванович"
            }
        }


class DisconnectParentResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате операции")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Связь успешно удалена",
            }
        }
