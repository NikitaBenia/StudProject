from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core.security import create_access_token, verify_token, oauth2_scheme
from app.schemas.user import User, UserDataForm, Token
from app.services.user_services import authenticate_user, register_user

router = APIRouter()

@router.post('/token', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='User data is invalid')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': form_data.username},
                                       expires_time=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

@router.post('/register', response_model=User)
def register(data: UserDataForm):
    user = register_user(data.username, data.password)
    return user