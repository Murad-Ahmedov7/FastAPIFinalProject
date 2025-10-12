from pydantic import BaseModel
from typing import List
from datetime import datetime
from .product_schema import ProductOut

# ====================
# OrderItem Schemas
# ====================
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float  # sifariş zamanı məhsulun qiyməti

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    product: ProductOut  # nested product info

    class Config:
        orm_mode = True

# ====================
# Order Schemas
# ====================
class OrderBase(BaseModel):
    status: str = "pending"  # pending, approved, rejected

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]  # basket-dən gələcək

class OrderResponse(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItemResponse] = []

class StatusUpdate(BaseModel):
    status: str

    class Config:
        from_attributes=True
