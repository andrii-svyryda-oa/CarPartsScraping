from pydantic import BaseModel
from datetime import datetime
import uuid

class CarModelBase(BaseModel):
    name: str
    year_from: datetime
    year_to: datetime
    body_type: str

class CarModelCreate(CarModelBase):
    brand_id: uuid.UUID

class CarModelUpdate(BaseModel):
    brand_id: uuid.UUID | None = None
    name: str | None = None
    year_from: datetime | None = None
    year_to: datetime | None = None
    body_type: str | None = None
