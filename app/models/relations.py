from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database.base import Base



class TeacherSubjectClass(Base):
    __tablename__ = "teacher_subject_class"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("teacher_id", "subject_id", "class_id", name="uq_teacher_subject_class"),)
