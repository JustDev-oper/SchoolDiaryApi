from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP
from app.database.base import Base


class Substitution(Base):
    __tablename__ = "substitutions"
    id = Column(Integer, primary_key=True, index=True)
    original_lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    new_teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    new_classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="SET NULL"))
    reason = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP)
