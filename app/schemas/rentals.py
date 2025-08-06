from pydantic import BaseModel

from datetime import datetime


class RentalCreate(BaseModel):
    car_id: int
    start_time: datetime
    end_time: datetime
