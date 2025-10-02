

from typing import Optional,List
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):

    username: str = Field( min_length=3, max_length=50)
    password: str = Field( min_length=6, max_length=128)
    email: str = Field(min_length=5, max_length=128)


class UserOut(BaseModel):
    id:int
    email: EmailStr
    username:str
    password:str
    class Config:
        from_attributes=True