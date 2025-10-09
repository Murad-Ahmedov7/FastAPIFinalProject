from pydantic import BaseModel
from typing import List

from schemas.product_schema import ProductOut


# Product schema

# ====================
# BasketItem Schemas
# ====================
class BasketItemBase(BaseModel):
    product_id: int
    quantity: int

class BasketItemCreate(BasketItemBase):
    pass

class BasketItemResponse(BasketItemBase):
    id: int
    product: ProductOut  # Nested product info

    class Config:
        orm_mode = True

# ====================
# Basket Schemas
# ====================
class BasketBase(BaseModel):
    user_id: int

class BasketCreate(BaseModel):
    items: List[BasketItemCreate] = []

class BasketResponse(BasketBase):
    id: int
    items: List[BasketItemResponse] = []

    class Config:
        from_attributes=True
