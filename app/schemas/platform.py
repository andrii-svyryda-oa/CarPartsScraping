from pydantic import BaseModel
from datetime import datetime
import uuid

class CreatePlatformIn(BaseModel):
    name: str
    base_url: str
    search_url_template: str
    is_active: bool = True

class UpdatePlatformIn(BaseModel):
    name: str | None = None
    base_url: str | None = None
    search_url_template: str | None = None
    is_active: bool | None = None

class PlatformOut(BaseModel):
    id: uuid.UUID
    name: str
    base_url: str
    search_url_template: str
    is_active: bool
    created_at: datetime
    updated_at: datetime 