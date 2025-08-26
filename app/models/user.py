from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, Date
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role_id = Column(Integer, ForeignKey("Roles.id", ondelete="RESTRICT"), nullable=False)
    login = Column(String(255), unique=True, index=True)
    created_at = Column(TIMESTAMP)
    date_of_birth = Column(Date, nullable=False)

    class_id = Column(Integer, ForeignKey("classes.id", ondelete="SET NULL"))

    role = relationship("Role")
    class_ = relationship("Class", back_populates="students")
