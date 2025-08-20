from sqlalchemy import Column, Integer, ForeignKey, Text, Date, TIMESTAMP, Enum, UniqueConstraint
from app.database.base import Base


class Homework(Base):
    __tablename__ = "homeworks"
    id = Column(Integer, primary_key=True, index=True)
    assigned_lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    due_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    max_grade = Column(Integer)


class HomeworkSubmission(Base):
    __tablename__ = "homework_submissions"
    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer, ForeignKey("homeworks.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    submitted_at = Column(TIMESTAMP)
    status = Column(Enum("not_submitted", "submitted", "graded", "late", name="submission_status"),
                    default="not_submitted")
    file_path = Column(Text)
    comment = Column(Text)

    __table_args__ = (UniqueConstraint("homework_id", "student_id"),)
