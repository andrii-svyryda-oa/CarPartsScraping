from pydantic import BaseModel
from datetime import datetime
import uuid

class CreateCarModelPlatformIn(BaseModel):
    car_model_id: uuid.UUID
    platform_id: uuid.UUID
    platform_url: str

class UpdateCarModelPlatformIn(BaseModel):
    car_model_id: uuid.UUID | None = None
    platform_id: uuid.UUID | None = None
    platform_url: str | None = None

class CarModelPlatformOut(BaseModel):
    id: uuid.UUID
    car_model_id: uuid.UUID
    platform_id: uuid.UUID
    platform_url: str
    created_at: datetime 