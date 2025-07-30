from pydantic import EmailStr
from datetime import timedelta
from app.schemas.users import User
from app.core.config import settings
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.security import create_access_token, verify_token
from fastapi import APIRouter, HTTPException, Request, Cookie, Form
from app.services.user_services import authenticate_user, register_user


router = APIRouter()

templates = Jinja2Templates(directory=settings.TEMPLATES_URL)


@router.get('/login')
def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/token')
def login(email: EmailStr = Form(...), password: str = Form(...)):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail='User data is invalid')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60   # Expires time for a cookie
    access_token = create_access_token(data={'sub': email},
                                       expires_time=access_token_expires)

    response = RedirectResponse('/', status_code=302)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        max_age=access_token_expires_seconds,
        secure=False
    )

    return response


def get_current_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


@router.get('/register')
def register_form(request: Request):
    return templates.TemplateResponse('signup.html', {'request': request})


@router.post('/register', response_model=User)
def register(fullname: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)):
    register_user(fullname, email, password)
    response = RedirectResponse('/login', status_code=303)
    return response