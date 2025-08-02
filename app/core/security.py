import datetime
from datetime import timedelta, datetime
from typing import Union

from fastapi import HTTPException
from passlib.context import CryptContext  # Used for password hashing and verification
from jose import jwt, JWTError  # Used for JWT encoding and decoding

from app.db.users import users
from app.core.config import settings


# Create a password hashing context using bcrypt
bcrypt_context = CryptContext(['bcrypt'], deprecated='auto')


# Create a JWT access token with optional expiration time
def create_access_token(data: dict, expires_time: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()

    # Set expiration time
    if expires_time:
        expire = datetime.utcnow() + expires_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire  # Add expiration field to payload

    # Encode the JWT with the given secret and algorithm
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encode_jwt


# Verify a plain password against its hashed version
def verify_password(password, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)


# Decode and verify a JWT token
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Check if token is valid and return corresponding user data
def verify_and_return_data(token: str) -> dict | None:
    if token:
        success_verify = verify_token(token)
        user = users.get_user(email=success_verify['sub'])  # Extract user using subject (email)
        return user
    return None


# Hash a plain password using bcrypt
def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)
