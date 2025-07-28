from fastapi import HTTPException
from app.schemas.user import User
from app.core.security import verify_password, get_hashed_password
from app.db.user import users, Users


def authenticate_user(username: str, password: str) -> str | None:
    user = users.get_user(username)
    if user and verify_password(password, user['hashed_password']):
        return user['hashed_password']
    return None

def register_user(username: str, password: str) -> User:
    users.add_user(username, password)
    user = users.get_user(username)
    if user and verify_password(password, user['hashed_password']):
        return User(username=user['username'], hashed_password=user['hashed_password'])
    else:
        raise HTTPException(status_code=401, detail='User data is invalid')
