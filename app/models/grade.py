from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, Enum, UniqueConstraint
from app.database.base import Base
import enum


class GradeEnum(str, enum.Enum):
    g2 = "2"
    g3 = "3"
    g4 = "4"
    g5 = "5"
    n = "н"
    b = "б"


class GradeType(str, enum.Enum):
    homework = "homework"
    test = "test"
    classwork = "classwork"
    oral = "oral"


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    grade = Column(Enum(GradeEnum), nullable=False)
    grade_type = Column(Enum(GradeType), nullable=False)
    comment = Column(Text)
    created_at = Column(TIMESTAMP)


class FinalGrade(Base):
    __tablename__ = "final_grades"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    grade = Column(Enum(GradeEnum), nullable=False)
    period_id = Column(Integer, ForeignKey("academic_periods.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("student_id", "subject_id", "period_id"),)
