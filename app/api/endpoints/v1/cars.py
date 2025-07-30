from app.schemas.cars import CarRemoveData
from fastapi import APIRouter, Form, UploadFile, File
from app.services.car_service import add_car as service_add_car
from app.services.car_service import remove_car as service_remove_car

router = APIRouter()


@router.post("/add_car")
def add_car(title: str = Form(...), price: float = Form(...), photo: UploadFile = File(...)):
    service_add_car(title, price, photo)
    return {'detail': 'Car created successfully'}


@router.post("/remove_car")
def remove_car(data: CarRemoveData):
    service_remove_car(id=data.id, title=data.title)
    return {'detail': 'Car deleted successfully'}