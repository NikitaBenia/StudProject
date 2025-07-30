from pydantic import BaseModel, EmailStr


class User(BaseModel):
    fullname: str
    email: EmailStr
    hashed_password: str


class UserAddDataForm(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserDataForm(BaseModel):
    email: EmailStr
    password: str