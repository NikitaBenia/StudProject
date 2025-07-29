from fastapi import HTTPException
from app.schemas.users import User
from app.core.security import verify_password
from app.db.users import users


def authenticate_user(username: str, password: str) -> str:
    user = users.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid password')
    return user['hashed_password']


def register_user(username: str, password: str) -> User:
    users.add_user(username, password)
    user = users.get_user(username)

    if not user:
        raise HTTPException(status_code=409, detail='User already exists')

    if user and verify_password(password, user['hashed_password']):
        return User(username=user['username'], hashed_password=user['hashed_password'])
    else:
        raise HTTPException(status_code=500, detail='Unexpected registration error')

