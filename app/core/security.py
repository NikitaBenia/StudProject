import datetime

from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core.config import settings

bcrypt_context = CryptContext(['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

def create_access_token(data: dict, expires_time: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()

    if expires_time:
        expire = datetime.utcnow() + expires_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encode_jwt

def verify_password(password, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return payload
    except JWTError:
        raise 'Invalid token'

def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)