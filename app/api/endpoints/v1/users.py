from datetime import timedelta

from pydantic import EmailStr
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File, Depends

from app.schemas.users import User
from app.core.config import settings
from app.core.security import create_access_token
from app.services.user_services import authenticate_user, register_user, change_user_avatar, get_user_page


router = APIRouter(tags=['User System'])


# Display login form (GET /login)
@router.get('/login')
def login_form(request: Request):
    from main import templates
    return templates.TemplateResponse('login.html', {'request': request})


# Handle login form submission, generate JWT, and set it as a cookie
@router.post('/token')
def login(email: EmailStr = Form(...),
          password: str = Form(...)):
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


# Display registration form (GET /register)
@router.get('/register')
def register_form(request: Request):
    from main import templates
    return templates.TemplateResponse('signup.html', {'request': request})


# Handle registration form submission, redirect to login
@router.post('/register', response_model=User)
def register(fullname: str = Form(...),
             email: EmailStr = Form(...),
             password: str = Form(...)):
    register_user(fullname, email, password)
    response = RedirectResponse('/login', status_code=303)
    return response


# Display user profile page after verifying JWT from cookie
@router.get('/profile', response_class=HTMLResponse)
def profile_page(request: Request, user = Depends(get_user_page)):
    from main import templates
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return templates.TemplateResponse('profile.html', {
        'request': request, 'user': user['user'], 'rentals': user['rentals']
    })


# Handle change the avatar of user, upload it to DataBase and response new profile
@router.post('/change_avatar')
def change_avatar(photo: UploadFile = File(...), user = Depends(get_user_page)):
    if not user:
        return RedirectResponse('/login', status_code=302)

    change_user_avatar(user['user'].get('email'), photo)
    response = RedirectResponse('/profile', status_code=302)
    return response
