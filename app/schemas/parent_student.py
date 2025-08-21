from pydantic import BaseModel, Field


class ParentConnectRequest(BaseModel):
    parent_id: int = Field(..., description="Id Родителя")
    student_id: int = Field(..., description="Id Учащегося")
    relationship: str = Field(..., description="Кто он для учащегося")

    class Config:
        json_schema_extra = {
            "example": {
                "parent_id": "1",
                "student_id": "2",
                "relationship": "father",
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


class DisconnectParentRequest(BaseModel):
    parent_id: int = Field(..., description="Id Родителя")
    student_id: int = Field(..., description="Id Учащегося")

    class Config:
        json_schema_extra = {
            "example": {
                "parent_id": "1",
                "student_id": "2",
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
