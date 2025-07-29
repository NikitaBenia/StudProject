from fastapi import UploadFile, HTTPException
from uuid import uuid4
from app.db.cars import cars
from app.core.config import settings

def add_car(title: str, price: float, photo: UploadFile):
    exist_car = cars.select_car(title=title)
    if exist_car:
        return exist_car

    filename = f"{uuid4().hex}_{photo.filename}"
    with open(settings.CAR_UPLOAD_URL / filename, "wb") as f:
        f.write(photo.file.read())

    return cars.add_car(title=title, price=price, photo=filename)


def remove_car(id: int, title: str):
    exist_car = cars.select_car(title=title)
    if not exist_car:
        raise HTTPException(status_code=404, detail='Car not found')

    file_path = settings.CAR_UPLOAD_URL / exist_car['photo']
    if file_path.exists():
        file_path.unlink()

    return cars.remove_car(id=id)