
from sqlalchemy import create_engine, Column, Integer, String
from database import Base


# SqlAlchemy Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)  # 🔹 yeni sütun