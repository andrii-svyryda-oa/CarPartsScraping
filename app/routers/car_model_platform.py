from fastapi import APIRouter, status
from app.dependencies.car_model_platform import CarModelPlatformCRUDDep, CarModelPlatformDep
from app.schemas.car_model_platform import CreateCarModelPlatformIn, UpdateCarModelPlatformIn, CarModelPlatformOut
from common.database.schemas.car_model_platform import CarModelPlatformCreate, CarModelPlatformUpdate

router = APIRouter(prefix="/car-model-platforms", tags=["car-model-platforms"])

@router.get("/", response_model=list[CarModelPlatformOut])
async def get_car_model_platforms(
    car_model_platform_crud: CarModelPlatformCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await car_model_platform_crud.get_multi(skip=skip, limit=limit)

@router.get("/{car_model_platform_id}", response_model=CarModelPlatformOut)
async def get_car_model_platform(car_model_platform: CarModelPlatformDep):
    return car_model_platform

@router.post("/", response_model=CarModelPlatformOut, status_code=status.HTTP_201_CREATED)
async def create_car_model_platform(
    car_model_platform_in: CreateCarModelPlatformIn,
    car_model_platform_crud: CarModelPlatformCRUDDep
):
    car_model_platform_create = CarModelPlatformCreate(**car_model_platform_in.model_dump())
    return await car_model_platform_crud.create(obj_in=car_model_platform_create)

@router.put("/{car_model_platform_id}", response_model=CarModelPlatformOut)
async def update_car_model_platform(
    car_model_platform: CarModelPlatformDep,
    car_model_platform_in: UpdateCarModelPlatformIn,
    car_model_platform_crud: CarModelPlatformCRUDDep
):
    car_model_platform_update = CarModelPlatformUpdate(**car_model_platform_in.model_dump(exclude_unset=True))
    return await car_model_platform_crud.update(db_obj=car_model_platform, obj_in=car_model_platform_update)

@router.delete("/{car_model_platform_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car_model_platform(car_model_platform: CarModelPlatformDep, car_model_platform_crud: CarModelPlatformCRUDDep):
    await car_model_platform_crud.remove(id=car_model_platform.id) 
