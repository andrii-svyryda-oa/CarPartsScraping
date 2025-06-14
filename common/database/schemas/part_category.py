from pydantic import BaseModel

class PartCategoryBase(BaseModel):
    name: str
    description: str

class PartCategoryCreate(PartCategoryBase):
    pass

class PartCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
