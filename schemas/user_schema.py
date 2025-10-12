

from typing import Optional,List
from pydantic import BaseModel, Field, EmailStr

from models.user import Role


class UserRegister(BaseModel):
    username: str
    email:EmailStr
    password:str=Field(min_length=6,max_length=128)
    role: Optional[Role]=Role.user

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    username:str
    role:Role
    is_active:bool

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str