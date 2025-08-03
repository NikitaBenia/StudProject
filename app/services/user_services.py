from uuid import uuid4
from fastapi import HTTPException, Request, UploadFile, File
from pydantic import EmailStr

from app.core.config import settings
from app.schemas.users import User
from app.core.security import verify_password, verify_and_return_data
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


def change_user_avatar(email: EmailStr, photo: UploadFile = File(...)):
    """
    Changing the avatar of user to new from upload file.

    - Check if the old avatar is default avatar
    - If it isn't delete them from static
    - Save new avatar to static
    - Update profile_icon in Data Base
    """
    user = users.get_user(email)

    old_avatar = user.get('profile_icon')
    if old_avatar and old_avatar != 'default.jpg':
        file_path = settings.ICON_UPLOAD_URL / old_avatar
        if file_path.exists():
            file_path.unlink()

    filename = f"{uuid4().hex}_{photo.filename}"
    with open(settings.ICON_UPLOAD_URL / filename, "wb") as f:
        f.write(photo.file.read())

    users.change_avatar(email, filename)


def get_user_page(request: Request):
    """
    Give the user found by access_token.

    - Check that token has not expired
    - Returning user or None if token was expired
    """
    access_token = request.cookies.get("access_token")
    user = verify_and_return_data(access_token)
    if not user:
        return None
    return user
