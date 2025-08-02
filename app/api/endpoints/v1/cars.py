from fastapi import APIRouter, Form, UploadFile, File, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.db.cars import cars
from app.db.cars_specs import cars_specs
from app.schemas.cars import CarRemoveData, CarSpecs
from app.services.car_service import add_car as service_add_car
from app.services.car_service import remove_car as service_remove_car


router = APIRouter()
templates = Jinja2Templates(directory=settings.TEMPLATES_URL)


# Parses car specifications from form data and returns a CarSpecs schema
def parse_car_specs_form(
    engine: str = Form(...),
    horsepower: int = Form(...),
    torque: int = Form(...),
    mph: float = Form(...),
    top_speed: int = Form(...),
    transmission: str = Form(...),
    drivetrain: str = Form(...),
    hybrid_system: str = Form(...),
    technology: str = Form(...),
    audio: str = Form(...),
    interior: str = Form(...),
    lighting: str = Form(...),
    comfort: str = Form(...),
    exterior: str = Form(...),
) -> CarSpecs:
    return CarSpecs(
        engine=engine,
        horsepower=horsepower,
        torque=torque,
        mph=mph,
        top_speed=top_speed,
        transmission=transmission,
        drivetrain=drivetrain,
        hybrid_system=hybrid_system,
        technology=technology,
        audio=audio,
        interior=interior,
        lighting=lighting,
        comfort=comfort,
        exterior=exterior,
    )


# Endpoint for adding a car (form fields + file upload + car specs)
@router.post("/add-car")
def add_car(
    title: str = Form(...),
    description: str = Form(...),
    city: str = Form(...),
    price: float = Form(...),
    photo: UploadFile = File(...),
    specs: CarSpecs = Depends(parse_car_specs_form)
):
    service_add_car(title, description, city, price, photo, specs)
    return {"detail": "Car created successfully"}


# Endpoint for removing a car by ID
@router.delete("/remove-car")
def remove_car(data: CarRemoveData):
    service_remove_car(id=data.id)
    return {"detail": "Car deleted successfully"}


# Renders the inventory HTML page with the list of all cars
@router.get("/inventory/", response_class=HTMLResponse)
def inventory(request: Request):
    all_cars = cars.select_all_cars()
    return templates.TemplateResponse("inventory.html", {"request": request, "cars": all_cars})


# Renders the details page for a specific car (includes car specs)
@router.get("/inventory/{car_id}", response_class=HTMLResponse)
def car_detail(request: Request, car_id: int):
    car = cars.select_car_by_id(car_id)
    car_specs = cars_specs.select_specs_by_car_id(car_id)

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    return templates.TemplateResponse(
        "car_detail.html",
        {"request": request, "car": car, "car_specs": car_specs}
    )
