from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy.sql.functions import current_user

from models import Order
from models.order import OrderItem
from models.user import User,Role
from schemas.order_schema import OrderCreate, OrderResponse,StatusUpdate  # əvvəlki token və role yoxlayan dependency
from deps import get_db, get_current_user,require_roles
from models.product import Product

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


# ==========================
# Create Order (User)
# ==========================
@router.post("/", response_model=OrderResponse,dependencies=[Depends(require_roles(Role.user,Role.admin))])
def create_order(
        order_in: OrderCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)

):
    order = Order(user_id=current_user.id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price  # sifariş zamanı məhsul qiyməti
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order


# ==========================
# Get Orders (User/Admin)
# ==========================
@router.get("/", response_model=List[OrderResponse],dependencies=[Depends(require_roles(Role.user,Role.admin))])
def get_orders(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role == Role.admin:  # admin bütün order-ları görür
        orders = db.query(Order).all()
    else:  # user yalnız öz order-larını görür
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


# ==========================
# Update Order Status (Admin)
# ==========================


@router.put("/{order_id}/status", response_model=OrderResponse,dependencies=[Depends(require_roles(Role.user,Role.admin))])
def update_order_status(
        order_id: int,
        payload: StatusUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Only admin can update status")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if payload.status not in ["pending", "approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    order.status = payload.status

    order.status = payload.status
    db.commit()
    db.refresh(order)
    return order
