from sqlalchemy import Column, Integer, String, Enum
from .database import Base

import enum

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False) 
    email = Column(String, unique=True, index=True, nullable=False) 
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
