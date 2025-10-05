from sqlalchemy import Column, Integer, String, Boolean

from database import Base


from sqlalchemy import Column, Integer, String, Boolean
from database import Base  # sənin declarative base-in

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    unique_stock_code = Column(String(100), nullable=False, unique=True)  # SKU
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
