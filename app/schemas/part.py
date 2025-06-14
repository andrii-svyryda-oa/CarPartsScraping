from pydantic import BaseModel
from datetime import datetime
import uuid

class CreatePartIn(BaseModel):
    oem_number: str
    name: str
    category_id: uuid.UUID
    manufacturer_id: uuid.UUID
    specifications: dict | None = None
    description: str | None = None

class UpdatePartIn(BaseModel):
    oem_number: str | None = None
    name: str | None = None
    category_id: uuid.UUID | None = None
    manufacturer_id: uuid.UUID | None = None
    specifications: dict | None = None
    description: str | None = None

class PartOut(BaseModel):
    id: uuid.UUID
    oem_number: str
    name: str
    category_id: uuid.UUID
    manufacturer_id: uuid.UUID
    specifications: dict | None
    description: str | None
    created_at: datetime 