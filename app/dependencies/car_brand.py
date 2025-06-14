from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.car_brand import CarBrandCRUD
from common.database.models.car_brand import CarBrand
import uuid

def get_car_brand_crud(db: DbDep) -> CarBrandCRUD:
    return CarBrandCRUD(db)

CarBrandCRUDDep = Annotated[CarBrandCRUD, Depends(get_car_brand_crud)]

async def get_car_brand_by_id(car_brand_id: uuid.UUID, car_brand_crud: CarBrandCRUDDep) -> CarBrand:
    car_brand = await car_brand_crud.get(car_brand_id)
    if not car_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car brand not found"
        )
    return car_brand

CarBrandDep = Annotated[CarBrand, Depends(get_car_brand_by_id)] 