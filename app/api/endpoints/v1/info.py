from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.services.user_services import get_user_page


router = APIRouter(tags=['Info Routes'])


@router.get('/insurance', response_class=HTMLResponse)
def insurance(request: Request, user = Depends(get_user_page)):
    from main import templates
    return templates.TemplateResponse('insurance.html', {
        'request': request, 'photo': user['user'].get('profile_icon')
    })


@router.get('/terms', response_class=HTMLResponse)
def terms(request: Request, user = Depends(get_user_page)):
    from main import templates
    return templates.TemplateResponse('terms.html', {
        'request': request, 'photo': user['user'].get('profile_icon')
    })


@router.get('/contact', response_class=HTMLResponse)
def contact(request: Request, user = Depends(get_user_page)):
    from main import templates
    return templates.TemplateResponse('contact.html', {
        'request': request, 'photo': user['user'].get('profile_icon')
    })