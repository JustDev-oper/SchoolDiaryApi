from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(10), unique=True, nullable=False)
    capacity = Column(Integer)
