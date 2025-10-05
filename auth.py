import os
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt, JWTError
import hashlib

SECRET_KEY = "CHANGE_ME_______STRONG_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") // bcrypt ile  ValueError: password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72]) error verir
#https://passlib.readthedocs.io/en/stable/narr/context-tutorial.html erroru burdan tapmaga calis
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(raw:str) ->str:
    return pwd_context.hash(raw)

def verify_password(raw:str, hashed:str)->bool:
    return pwd_context.verify(raw,hashed)


def create_access_token(sub: str, role: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    now = datetime.utcnow()
    payload = {
        'sub': sub,
        'role': role,
        'iat': now,
        'exp': now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
