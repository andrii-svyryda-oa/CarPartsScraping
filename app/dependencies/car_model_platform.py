from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.car_model_platform import CarModelPlatformCRUD
from common.database.models.car_model_platform import CarModelPlatform
import uuid

def get_car_model_platform_crud(db: DbDep) -> CarModelPlatformCRUD:
    return CarModelPlatformCRUD(db)

CarModelPlatformCRUDDep = Annotated[CarModelPlatformCRUD, Depends(get_car_model_platform_crud)]

async def get_car_model_platform_by_id(car_model_platform_id: uuid.UUID, car_model_platform_crud: CarModelPlatformCRUDDep) -> CarModelPlatform:
    car_model_platform = await car_model_platform_crud.get(car_model_platform_id)
    if not car_model_platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car model platform association not found"
        )
    return car_model_platform

CarModelPlatformDep = Annotated[CarModelPlatform, Depends(get_car_model_platform_by_id)] 