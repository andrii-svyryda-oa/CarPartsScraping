from pydantic import BaseModel

class PartCategoryBase(BaseModel):
    name: str
    description: str
    possible_names: list[str]

class PartCategoryCreate(PartCategoryBase):
    pass

class PartCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    possible_names: list[str] | None = None
