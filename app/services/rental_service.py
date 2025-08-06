from datetime import datetime

from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from app.db.cars import cars
from app.db.rentals import rentals
from app.db.users import users


def get_full_price(car_id: int, start_time: str, end_time: str):
    """
    Get full price of car rent.

    - Check the car existing
    - Check a validation data of times
    - Transform the date to dd.mm.yyyy HH:MM type
    - Calculating the subtotal, taxes and total
    """

    car = cars.select_car_by_id(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if start_time >= end_time:
        return RedirectResponse(f'/inventory/{car_id}')

    start_date = datetime.fromisoformat(start_time).date()
    end_date = datetime.fromisoformat(end_time).date()

    now_time = datetime.utcnow().time()

    start_dt = datetime.combine(start_date, now_time)
    end_dt = datetime.combine(end_date, now_time)

    rental_days = (end_dt - start_dt).days
    subtotal = rental_days * car.get('price')
    taxes = round(subtotal * 0.075, 2)
    total = round(subtotal + taxes, 2)

    return {
        'total': total,
        'taxes': taxes,
        'subtotal': subtotal,
        'rental_days': rental_days,
        'start_dt': start_dt,
        'end_dt': end_dt,
        'car': car
    }


def add_rental(car_id: int, user_id: int, total_price: float, start_time: datetime, end_time: datetime):
    """
    Add the rent to user.

    - Check the validation of times
    - Check the user and car existing
    - Check the balance of user to make a payment
    - Make a payment from user balance
    """
    if start_time >= end_time:
        raise HTTPException(status_code=422, detail='Invalid rental dates')

    car = cars.select_car_by_id(car_id)
    if not car:
        raise HTTPException(status_code=404, detail='Car not found')

    user = users.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    new_balance = user.get('balance') - total_price

    if new_balance < 0:
        raise HTTPException(status_code=400, detail='Not enough balance')

    users.change_balance(user.get('email'), new_balance)

    rentals.add_rental(car_id, user.get('id'), start_time, end_time)
