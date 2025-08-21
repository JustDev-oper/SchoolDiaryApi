import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, UniqueConstraint

from app.database.base import Base


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
