from pydantic import BaseModel
import uuid

class CarModelPlatformBase(BaseModel):
    platform_url: str

class CarModelPlatformCreate(CarModelPlatformBase):
    car_model_id: uuid.UUID
    platform_id: uuid.UUID

class CarModelPlatformUpdate(BaseModel):
    car_model_id: uuid.UUID | None = None
    platform_id: uuid.UUID | None = None
    platform_url: str | None = None
