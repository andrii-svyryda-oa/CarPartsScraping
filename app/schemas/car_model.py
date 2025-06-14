from pydantic import BaseModel
from datetime import datetime
import uuid

class CreateCarModelIn(BaseModel):
    brand_id: uuid.UUID
    name: str
    year_from: datetime
    year_to: datetime
    body_type: str

class UpdateCarModelIn(BaseModel):
    brand_id: uuid.UUID | None = None
    name: str | None = None
    year_from: datetime | None = None
    year_to: datetime | None = None
    body_type: str | None = None

class CarModelOut(BaseModel):
    id: uuid.UUID
    brand_id: uuid.UUID
    name: str
    year_from: datetime
    year_to: datetime
    body_type: str
    created_at: datetime 