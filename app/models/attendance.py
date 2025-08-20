from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, UniqueConstraint
from app.database.base import Base
import enum


class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    reason = Column(Text)

    __table_args__ = (UniqueConstraint("student_id", "lesson_id"),)
