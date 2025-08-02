from fastapi import HTTPException
from pydantic import EmailStr

from app.schemas.users import User
from app.core.security import verify_password
from app.db.users import users


def authenticate_user(email: EmailStr, password: str) -> str:
    """
    Authenticate a user by email and password.

    - Retrieve the user record by email.
    - If user not found, raise 404 Not Found.
    - Verify the provided password against the stored hashed password.
    - If password is invalid, raise 401 Unauthorized.
    - Return the hashed password on successful authentication.
    """
    user = users.get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid password')
    return user['hashed_password']


def register_user(fullname: str, email: EmailStr, password: str) -> User:
    """
    Register a new user with fullname, email, and password.

    - Check if a user with the given email already exists.
    - If user exists, raise 409 Conflict.
    - Otherwise, create a new user and store the hashed password.
    - Return a User schema instance representing the new user.
    """
    exist_user = users.get_user(email)

    if not exist_user:
        hashed_password = users.add_user(fullname, email, password)
        return User(fullname=fullname, email=email, hashed_password=hashed_password)

    raise HTTPException(status_code=409, detail='User already exists')
