from pydantic import BaseModel
from datetime import datetime
import uuid

class CreateCarBrandIn(BaseModel):
    name: str
    country_origin: str

class UpdateCarBrandIn(BaseModel):
    name: str | None = None
    country_origin: str | None = None

class CarBrandOut(BaseModel):
    id: uuid.UUID
    name: str
    country_origin: str
    created_at: datetime 