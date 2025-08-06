from pydantic import BaseModel


class CarSpecs(BaseModel):
    engine: str
    horsepower: int
    torque: int
    mph: float
    top_speed: int
    transmission: str
    drivetrain: str
    hybrid_system: str
    technology: str
    audio: str
    interior: str
    lighting: str
    comfort: str
    exterior: str


class CarCreate(BaseModel):
    title: str
    description: str
    city: str
    price: float
    specs: CarSpecs


class CarRemoveData(BaseModel):
    id: int
