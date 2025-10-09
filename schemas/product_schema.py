from pydantic import BaseModel,Field
from slugify import slugify
class ProductIn(BaseModel):
    name: str
    unique_stock_code:str=Field(min_length=5)
    description:str=Field(min_length=5)
    price:float
    quantity:int


class ProductOut(BaseModel):
    id:int
    name: str
    unique_stock_code:str
    description:str
    price:float
    quantity:int
    is_active:bool
    slug:str

    class Config:
        from_attributes = True

