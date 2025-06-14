from fastapi import APIRouter, status
from app.dependencies.car_brand import CarBrandCRUDDep, CarBrandDep
from app.schemas.car_brand import CreateCarBrandIn, UpdateCarBrandIn, CarBrandOut
from common.database.schemas.car_brand import CarBrandCreate, CarBrandUpdate

router = APIRouter(prefix="/car-brands", tags=["car-brands"])

@router.get("/", response_model=list[CarBrandOut])
async def get_car_brands(
    car_brand_crud: CarBrandCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await car_brand_crud.get_multi(skip=skip, limit=limit)

@router.get("/{car_brand_id}", response_model=CarBrandOut)
async def get_car_brand(car_brand: CarBrandDep):
    return car_brand

@router.post("/", response_model=CarBrandOut, status_code=status.HTTP_201_CREATED)
async def create_car_brand(
    car_brand_in: CreateCarBrandIn,
    car_brand_crud: CarBrandCRUDDep
):
    car_brand_create = CarBrandCreate(**car_brand_in.model_dump())
    return await car_brand_crud.create(obj_in=car_brand_create)

@router.put("/{car_brand_id}", response_model=CarBrandOut)
async def update_car_brand(
    car_brand: CarBrandDep,
    car_brand_in: UpdateCarBrandIn,
    car_brand_crud: CarBrandCRUDDep
):
    car_brand_update = CarBrandUpdate(**car_brand_in.model_dump(exclude_unset=True))
    return await car_brand_crud.update(db_obj=car_brand, obj_in=car_brand_update)

@router.delete("/{car_brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car_brand(car_brand: CarBrandDep, car_brand_crud: CarBrandCRUDDep):
    await car_brand_crud.remove(id=car_brand.id) 