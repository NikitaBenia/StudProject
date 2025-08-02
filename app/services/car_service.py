from fastapi import UploadFile, HTTPException
from uuid import uuid4

from app.db.cars import cars
from app.db.cars_specs import cars_specs
from app.core.config import settings
from app.schemas.cars import CarSpecs


def add_car(title: str, description: str, city: str, price: float, photo: UploadFile, specs: CarSpecs):
    """
    Adds a new car with its specifications and saves the uploaded photo to disk.

    Steps:
    - Check if a car with the given title already exists; if yes, raise HTTP 409 Conflict.
    - Generate a unique filename using UUID and original filename to avoid collisions.
    - Save the uploaded photo file to the configured upload directory.
    - Add the car record to the database, storing the photo filename.
    - Add the car's specifications to the database linked by car_id.
    """

    exist_car = cars.select_car_by_title(title=title)
    if exist_car:
        raise HTTPException(status_code=409, detail='Car is already exist')

    filename = f"{uuid4().hex}_{photo.filename}"
    with open(settings.CAR_UPLOAD_URL / filename, "wb") as f:
        f.write(photo.file.read())

    car = cars.add_car(title=title, description=description, city=city, price=price, photo=filename)

    cars_specs.add_specs(
        car_id=car,
        engine=specs.engine,
        horsepower=specs.horsepower,
        torque=specs.torque,
        mph=specs.mph,
        top_speed=specs.top_speed,
        transmission=specs.transmission,
        drivetrain=specs.drivetrain,
        hybrid_system=specs.hybrid_system,
        technology=specs.technology,
        audio=specs.audio,
        interior=specs.interior,
        lighting=specs.lighting,
        comfort=specs.comfort,
        exterior=specs.exterior
    )


def remove_car(id: int):
    """
    Removes a car by its ID.

    Steps:
    - Check if the car with given ID exists; if not, raise HTTP 404 Not Found.
    - Delete the associated photo file from disk if it exists.
    - Remove the car record from the database.
    - Return the result of the remove operation.
    """

    exist_car = cars.select_car_by_id(id=id)
    if not exist_car:
        raise HTTPException(status_code=404, detail='Car not found')

    file_path = settings.CAR_UPLOAD_URL / exist_car['photo']
    if file_path.exists():
        file_path.unlink()

    return cars.remove_car(id=id)
