from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.car_model import CarModelCRUD
from common.database.models.car_model import CarModel
import uuid

def get_car_model_crud(db: DbDep) -> CarModelCRUD:
    return CarModelCRUD(db)

CarModelCRUDDep = Annotated[CarModelCRUD, Depends(get_car_model_crud)]

async def get_car_model_by_id(car_model_id: uuid.UUID, car_model_crud: CarModelCRUDDep) -> CarModel:
    car_model = await car_model_crud.get(car_model_id)
    if not car_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car model not found"
        )
    return car_model

CarModelDep = Annotated[CarModel, Depends(get_car_model_by_id)] 