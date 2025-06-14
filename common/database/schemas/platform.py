from pydantic import BaseModel

class PlatformBase(BaseModel):
    name: str
    base_url: str
    search_url_template: str
    is_active: bool = True

class PlatformCreate(PlatformBase):
    pass

class PlatformUpdate(BaseModel):
    name: str | None = None
    base_url: str | None = None
    search_url_template: str | None = None
    is_active: bool | None = None
