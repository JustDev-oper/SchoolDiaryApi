from sqlalchemy import Integer, Column, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database.base import Base


class FinalGrade(Base):
    __tablename__ = 'final_grades'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    grade = Column(Enum('2', '3', '4', '5'), nullable=False)
    period_id = Column(Integer, ForeignKey('academic_periods.id'), nullable=False)

    # Обратные отношения
    student = relationship('User', back_populates='final_grades')
    subject = relationship('Subject', back_populates='final_grades')
    class_ = relationship('Class', back_populates='final_grades')
    period = relationship('AcademicPeriod', back_populates='final_grades')
