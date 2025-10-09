from typing import List

from fastapi import Depends, HTTPException, APIRouter
from slugify import slugify
from sqlalchemy.orm import Session
from deps import get_db, require_roles
from models.product import Product
from models.user import Role
from schemas.product_schema import ProductOut, ProductIn
from fastapi import Response

router=APIRouter(prefix="/api/admin/products", tags=["admin_products"])


@router.post('/add',response_model=ProductOut,dependencies=[Depends(require_roles(Role.admin))],status_code=201)
def add(payload:ProductIn,db:Session=Depends(get_db)):
    product=Product(name=payload.name,unique_stock_code=payload.unique_stock_code,description=payload.description,price=payload.price,quantity=payload.quantity,slug=slugify(payload.name))
    db.add(product)
    db.commit()
    db.refresh(product)
    return product



@router.get('/',response_model=List[ProductOut],dependencies=[Depends(require_roles(Role.admin))],status_code=200)
def getAllProducts(db:Session=Depends(get_db)):
    return  db.query(Product).all()




@router.post('/update/{product_id}', response_model=ProductOut, dependencies=[Depends(require_roles(Role.admin))])
def update(product_id: int, payload: ProductIn, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = payload.name
    product.unique_stock_code = payload.unique_stock_code
    product.description = payload.description
    product.price = payload.price
    product.quantity = payload.quantity
    product.slug = slugify(payload.name)

    db.commit()
    db.refresh(product)
    return product

@router.delete('/delete/{product_id}', status_code=204,dependencies=[Depends(require_roles(Role.admin))])
def delete(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return Response(status_code=204)
#slug tekrarlanmasin qarsini al


#token vaxt bitmesi