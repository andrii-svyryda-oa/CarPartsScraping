from fastapi import APIRouter, status
from app.dependencies.car_model import CarModelCRUDDep, CarModelDep
from app.schemas.car_model import CreateCarModelIn, UpdateCarModelIn, CarModelOut
from common.database.schemas.car_model import CarModelCreate, CarModelUpdate

router = APIRouter(prefix="/car-models", tags=["car-models"])

@router.get("/", response_model=list[CarModelOut])
async def get_car_models(
    car_model_crud: CarModelCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await car_model_crud.get_multi(skip=skip, limit=limit)

@router.get("/{car_model_id}", response_model=CarModelOut)
async def get_car_model(car_model: CarModelDep):
    return car_model

@router.post("/", response_model=CarModelOut, status_code=status.HTTP_201_CREATED)
async def create_car_model(
    car_model_in: CreateCarModelIn,
    car_model_crud: CarModelCRUDDep
):
    car_model_create = CarModelCreate(**car_model_in.model_dump())
    return await car_model_crud.create(obj_in=car_model_create)

@router.put("/{car_model_id}", response_model=CarModelOut)
async def update_car_model(
    car_model: CarModelDep,
    car_model_in: UpdateCarModelIn,
    car_model_crud: CarModelCRUDDep
):
    car_model_update = CarModelUpdate(**car_model_in.model_dump(exclude_unset=True))
    return await car_model_crud.update(db_obj=car_model, obj_in=car_model_update)

@router.delete("/{car_model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car_model(car_model: CarModelDep, car_model_crud: CarModelCRUDDep):
    await car_model_crud.remove(id=car_model.id) 