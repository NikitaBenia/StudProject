from fastapi import APIRouter, Request, Query, HTTPException, Form, Cookie, Depends
from fastapi.responses import RedirectResponse, HTMLResponse

from app.db.users import users
from app.services.rental_service import add_rental as service_add_rental
from app.services.rental_service import get_full_price
from app.services.user_services import get_user_page


router = APIRouter(tags=['Rental System'])


# Display checkout page with already calculated price and taxed
@router.get("/checkout", response_class=HTMLResponse)
def checkout(
        request: Request,
        car_id: int = Query(...),
        start_time: str = Query(...),
        end_time: str = Query(...),
        user = Depends(get_user_page)
):
    from main import templates

    if not user:
        return RedirectResponse('/login', status_code=302)

    full_price = get_full_price(car_id, start_time, end_time)

    return templates.TemplateResponse("checkout.html", {
        "request": request,
        "car": full_price.get('car'),
        "start_time": start_time,
        "end_time": end_time,
        "rental_days": full_price.get('rental_days'),
        "subtotal": full_price.get('subtotal'),
        "taxes": full_price.get('taxes'),
        "total": full_price.get('total')
    })



# Handle to add the rental to user
@router.post("/checkout")
def add_rental(
    car_id: int = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    email: str = Form(...),
    user = Depends(get_user_page)
):
    if not user:
        return RedirectResponse('/login', status_code=302)

    existing_user = users.get_user(email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User with provided email not found"
        )

    full_price = get_full_price(car_id, start_time, end_time)

    service_add_rental(
        car_id,
        user['user'].get('id'),
        full_price.get('total'),
        full_price.get('start_dt'),
        full_price.get('end_dt')
    )

    return RedirectResponse('/', status_code=303)
