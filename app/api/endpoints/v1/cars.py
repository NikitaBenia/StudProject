from fastapi import APIRouter, Form, UploadFile, File, Depends, Request, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.db.cars import cars
from app.db.cars_specs import cars_specs
from app.schemas.cars import CarRemoveData, CarSpecs
from app.services.car_service import add_car as service_add_car
from app.services.car_service import remove_car as service_remove_car
from app.services.user_services import get_user_page


router = APIRouter()


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
def inventory(
    request: Request,
    user = Depends(get_user_page),
    title: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    from main import templates
    filtered_cars = cars.select_filtered_cars(title=title, city=city)

    if not user:
        return templates.TemplateResponse(
            "inventory.html", {"request": request, "cars": filtered_cars}
        )
    return templates.TemplateResponse(
        "inventory.html", {"request": request, "photo": user.get('profile_icon'), "cars": filtered_cars}
    )


# Renders the details page for a specific car (includes car specs)
@router.get("/inventory/{car_id}", response_class=HTMLResponse)
def car_detail(request: Request, car_id: int, user = Depends(get_user_page)):
    from main import templates
    car = cars.select_car_by_id(car_id)
    car_specs = cars_specs.select_specs_by_car_id(car_id)

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if not user:
        return templates.TemplateResponse(
            "car_detail.html",
            {"request": request, "car": car, "car_specs": car_specs}
        )
    return templates.TemplateResponse(
        "car_detail.html",
        {"request": request, "photo": user.get('profile_icon'), "car": car, "car_specs": car_specs}
    )
