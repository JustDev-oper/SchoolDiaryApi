from pydantic import Field, BaseModel


class ClassCreateRequest(BaseModel):
    name: str = Field(..., description="Имя класса")
    academic_year: str = Field(..., description="Период учебы")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "11А",
                "academic_year": "2018/2019",
            }
        }


class ClassCreateResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате операции")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Успешно"
            }
        }


class DeleteClassResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате операции")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Успешно"
            }
        }


class ClassResponse(BaseModel):
    id: int
    name: str
    academic_year: str
