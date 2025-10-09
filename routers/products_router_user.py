from typing import List

from fastapi import Depends, HTTPException, APIRouter
from slugify import slugify
from sqlalchemy.orm import Session
from deps import get_db, require_roles
from models.product import Product
from models.user import Role
from schemas.product_schema import ProductOut, ProductIn

router = APIRouter(prefix="/api/user/products", tags=["user_products"])


@router.get('/', response_model=List[ProductOut], status_code=200)
def get_all_products_for_user(db: Session = Depends(get_db)):
    return db.query(Product).all()
