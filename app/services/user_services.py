from fastapi import HTTPException
from pydantic import EmailStr
from app.schemas.users import User
from app.core.security import verify_password
from app.db.users import users


def authenticate_user(email: EmailStr, password: str) -> str:
    user = users.get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid password')
    return user['hashed_password']


def register_user(fullname: str, email: EmailStr, password: str) -> User:
    exist_user = users.get_user(email)

    if not exist_user:
        hashed_password = users.add_user(fullname, email, password)
        return User(fullname=fullname, email=email, hashed_password=hashed_password)

    raise HTTPException(status_code=409, detail='User already exists')
