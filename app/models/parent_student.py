from sqlalchemy import Column, Integer, ForeignKey

from app.database.base import Base

class ParentStudent(Base):
    __tablename__ = 'parent_student'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent_student.id'))