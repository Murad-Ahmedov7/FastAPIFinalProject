import enum

from sqlalchemy import create_engine, Column, Integer, String, Enum as SAEnum, Boolean
from database import Base

class Role(str,enum.Enum):
    admin="admin"
    user="user"



# SqlAlchemy Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash=Column(String(255),nullable=False)
    role = Column(SAEnum(Role), nullable=False, default=Role.user)
    is_active= Column(Boolean, nullable=False, default=True)