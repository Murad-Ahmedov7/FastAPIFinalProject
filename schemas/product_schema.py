from pydantic import BaseModel,Field
from slugify import slugify
class ProductIn(BaseModel):
    name: str
    unique_stock_code:str=Field(min_length=5)
    description:str=Field(min_length=5)
    price:float
    quantity:int


class ProductOut(BaseModel):
    name: str
    unique_stock_code:str
    description:str
    price:float
    quantity:int
    is_active:bool
    slug:str
    class Config:
        from_attributes=True

    # name = Column(String(200), nullable=False)
    # slug = Column(String(200), nullable=False, unique=True)
    # unique_stock_code = Column(String(100), nullable=False, unique=True)  # SKU
    # description = Column(String, nullable=True)
    # price = Column(Integer, nullable=False, default=0)
    # quantity = Column(Integer, nullable=False, default=0)
    # is_active = Column(Boolean, nullable=False, default=True)
