from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database.base import Base


class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # например "9А"
    academic_year = Column(String(9), nullable=False)  # например "2024/2025"

    students = relationship("User", back_populates="class_")
