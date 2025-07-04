from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    role: UserRole = UserRole.user

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True
