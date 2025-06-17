from fastapi import APIRouter, status
from app.dependencies.part_manufacturer import PartManufacturerCRUDDep, PartManufacturerDep
from app.schemas.part_manufacturer import CreatePartManufacturerIn, UpdatePartManufacturerIn, PartManufacturerOut
from common.database.schemas.part_manufacturer import PartManufacturerCreate, PartManufacturerUpdate

router = APIRouter(prefix="/part-manufacturers", tags=["part-manufacturers"])


@router.get("", response_model=list[PartManufacturerOut])
async def get_part_manufacturers(
    part_manufacturer_crud: PartManufacturerCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await part_manufacturer_crud.get_multi(skip=skip, limit=limit)


@router.get("/{part_manufacturer_id}", response_model=PartManufacturerOut)
async def get_part_manufacturer(part_manufacturer: PartManufacturerDep):
    return part_manufacturer


@router.post("", response_model=PartManufacturerOut, status_code=status.HTTP_201_CREATED)
async def create_part_manufacturer(
    part_manufacturer_in: CreatePartManufacturerIn,
    part_manufacturer_crud: PartManufacturerCRUDDep
):
    part_manufacturer_create = PartManufacturerCreate(**part_manufacturer_in.model_dump())
    return await part_manufacturer_crud.create(obj_in=part_manufacturer_create)


@router.put("/{part_manufacturer_id}", response_model=PartManufacturerOut)
async def update_part_manufacturer(
    part_manufacturer: PartManufacturerDep,
    part_manufacturer_in: UpdatePartManufacturerIn,
    part_manufacturer_crud: PartManufacturerCRUDDep
):
    part_manufacturer_update = PartManufacturerUpdate(**part_manufacturer_in.model_dump(exclude_unset=True))
    return await part_manufacturer_crud.update(db_obj=part_manufacturer, obj_in=part_manufacturer_update)


@router.delete("/{part_manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_part_manufacturer(part_manufacturer: PartManufacturerDep, part_manufacturer_crud: PartManufacturerCRUDDep):
    await part_manufacturer_crud.remove(id=part_manufacturer.id) 
    