from sqlalchemy import Column, Integer, Enum, ForeignKey, UniqueConstraint
from app.database.base import Base
import enum


class RelationshipEnum(str, enum.Enum):
    mother = "mother"
    father = "father"
    guardian = "guardian"
    other = "other"


class ParentStudent(Base):
    __tablename__ = "parent_student"
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    relationship = Column(Enum(RelationshipEnum), nullable=False)

    __table_args__ = (UniqueConstraint("parent_id", "student_id", name="uq_parent_student"),)


class TeacherSubjectClass(Base):
    __tablename__ = "teacher_subject_class"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("teacher_id", "subject_id", "class_id", name="uq_teacher_subject_class"),)
