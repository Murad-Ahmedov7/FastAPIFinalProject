from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from deps import get_db, get_current_user, require_roles
from models.basket import Basket, BasketItem
from models.user import User, Role
from models.product import Product
from schemas.basket_schema import BasketItemCreate, BasketItemResponse, BasketResponse

router = APIRouter(prefix="/api/user/basket", tags=["basket"])

# --------------------------
# GET Basket (show all items)
# --------------------------
@router.get("/", response_model=BasketResponse, dependencies=[Depends(require_roles(Role.user))])
def get_basket(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket:
        # boş basket yaradırıq
        basket = Basket(user_id=current_user.id)
        db.add(basket)
        db.commit()
        db.refresh(basket)
    return basket

# --------------------------
# Add item to Basket
# --------------------------
@router.post("/items/", response_model=BasketItemResponse, dependencies=[Depends(require_roles(Role.user))])
def add_to_basket(
    payload: BasketItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket:
        basket = Basket(user_id=current_user.id)
        db.add(basket)
        db.commit()
        db.refresh(basket)

    product = db.query(Product).filter(Product.id == payload.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if payload.quantity > product.quantity:
        raise HTTPException(status_code=400, detail=f"Only {product.quantity} items in stock")

    basket_item = db.query(BasketItem).filter(
        BasketItem.basket_id == basket.id,
        BasketItem.product_id == product.id
    ).first()

    if basket_item:
        basket_item.quantity += payload.quantity
    else:
        basket_item = BasketItem(
            basket_id=basket.id,
            product_id=product.id,
            quantity=payload.quantity
        )
        db.add(basket_item)

    db.commit()
    db.refresh(basket_item)
    return basket_item

# --------------------------
# Update Basket Item quantity
# --------------------------
@router.put("/items/{item_id}", response_model=BasketItemResponse, dependencies=[Depends(require_roles(Role.user))])
def update_basket_item(
    item_id: int,
    payload: BasketItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket_item = db.query(BasketItem).filter(
        BasketItem.id == item_id,
        BasketItem.basket_id == basket.id
    ).first()
    if not basket_item:
        raise HTTPException(status_code=404, detail="Basket item not found")

    product = db.query(Product).filter(Product.id == basket_item.product_id).first()
    if payload.quantity > product.quantity:
        raise HTTPException(status_code=400, detail=f"Only {product.quantity} items in stock")

    basket_item.quantity = payload.quantity
    db.commit()
    db.refresh(basket_item)
    return basket_item

# --------------------------
# Delete Basket Item
# --------------------------
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(Role.user))])
def delete_basket_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket_item = db.query(BasketItem).filter(
        BasketItem.id == item_id,
        BasketItem.basket_id == basket.id
    ).first()
    if not basket_item:
        raise HTTPException(status_code=404, detail="Basket item not found")

    db.delete(basket_item)
    db.commit()
    return
