

from fastapi import Depends, HTTPException, APIRouter
from slugify import slugify
from sqlalchemy.orm import Session
from deps import get_db, require_roles
from models.product import Product
from models.user import Role
from schemas.product_schema import ProductOut, ProductIn

router=APIRouter(prefix="/api/admin/products", tags=["products"])

@router.post('/add',response_model=ProductOut,dependencies=[Depends(require_roles(Role.admin))],status_code=201)
def add(payload:ProductIn,db:Session=Depends(get_db)):
    product=Product(name=payload.name,unique_stock_code=payload.unique_stock_code,description=payload.description,price=payload.price,quantity=payload.quantity,slug=slugify(payload.name))
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


#slug tekrarlanmasin qarsini al