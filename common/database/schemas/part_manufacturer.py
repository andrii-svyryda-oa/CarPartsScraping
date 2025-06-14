from pydantic import BaseModel

class PartManufacturerBase(BaseModel):
    name: str
    description: str

class PartManufacturerCreate(PartManufacturerBase):
    pass

class PartManufacturerUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
