from pydantic import BaseModel
from datetime import datetime
import uuid

class CreatePartManufacturerIn(BaseModel):
    name: str
    description: str

class UpdatePartManufacturerIn(BaseModel):
    name: str | None = None
    description: str | None = None

class PartManufacturerOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime 