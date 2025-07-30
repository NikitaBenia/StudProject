import datetime
from typing import Union
from jose import jwt, JWTError
from app.db.users import users
from app.core.config import settings
from datetime import timedelta, datetime
from passlib.context import CryptContext

bcrypt_context = CryptContext(['bcrypt'], deprecated='auto')


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


def verify_and_return_data(token: str) -> dict | None:
    if token:
        success_verify = verify_token(token)
        user = users.get_user(email=success_verify['sub'])
        return user
    return None


def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)