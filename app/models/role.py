from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Role(Base):
    __tablename__ = "Roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
