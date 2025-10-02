from http.client import responses

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from deps import get_db
from models.user import User
from schemas.user_schema import UserOut,UserCreate

router=APIRouter(prefix="/api/users",tags=["users"])

@router.post('/',response_model=UserOut,status_code=201)
def create_author(payload:UserCreate,db:Session=Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut.from_orm(user)
