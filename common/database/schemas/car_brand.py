from pydantic import BaseModel

class CarBrandBase(BaseModel):
    name: str
    country_origin: str

class CarBrandCreate(CarBrandBase):
    pass

class CarBrandUpdate(BaseModel):
    name: str | None = None
    country_origin: str | None = None
