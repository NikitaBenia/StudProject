from pydantic import BaseModel

class CarRemoveData(BaseModel):
    id: int
    title: str