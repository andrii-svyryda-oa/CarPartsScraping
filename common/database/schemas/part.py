from pydantic import BaseModel
import uuid

class PartBase(BaseModel):
    oem_number: str
    name: str
    specifications: dict | None = None
    description: str | None = None

class PartCreate(PartBase):
    category_id: uuid.UUID
    manufacturer_id: uuid.UUID

class PartUpdate(BaseModel):
    oem_number: str | None = None
    name: str | None = None
    category_id: uuid.UUID | None = None
    manufacturer_id: uuid.UUID | None = None
    specifications: dict | None = None
    description: str | None = None
