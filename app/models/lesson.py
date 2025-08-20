from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text, Date, UniqueConstraint
from app.database.base import Base


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    lesson_number = Column(Integer, nullable=False)
    topic = Column(Text)
    is_substitution = Column(Boolean, default=False)
    substitute_teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    __table_args__ = (
        UniqueConstraint("class_id", "date", "lesson_number"),
        UniqueConstraint("teacher_id", "date", "lesson_number"),
        UniqueConstraint("substitute_teacher_id", "date", "lesson_number"),
        UniqueConstraint("classroom_id", "date", "lesson_number"),
    )
