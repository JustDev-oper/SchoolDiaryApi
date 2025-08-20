import enum

from sqlalchemy import Column, String, Integer, Enum, Date

from app.database.base import Base


class PeriodType(str, enum.Enum):
    quarter = "quarter"
    semester = "semester"
    year = "year"


class AcademicPeriod(Base):
    __tablename__ = "academic_periods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    academic_year = Column(String(9), nullable=False)
    type = Column(Enum(PeriodType), nullable=False)
