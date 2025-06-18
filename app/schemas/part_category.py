from pydantic import BaseModel
from datetime import datetime
import uuid

class CreatePartCategoryIn(BaseModel):
    name: str
    description: str
    possible_names: list[str]

class UpdatePartCategoryIn(BaseModel):
    name: str | None = None
    description: str | None = None
    possible_names: list[str] | None = None

class PartCategoryOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime 
    possible_names: list[str]
