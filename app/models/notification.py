from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP, Enum
from app.database.base import Base
import enum


class NotificationType(str, enum.Enum):
    grade = "grade"
    attendance = "attendance"
    homework = "homework"
    substitution = "substitution"
    system = "system"


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    is_read = Column(Boolean, default=False)
    related_id = Column(Integer)
    created_at = Column(TIMESTAMP)
