from fastapi import APIRouter, status
from app.dependencies.part import PartCRUDDep, PartDep
from app.schemas.part import CreatePartIn, UpdatePartIn, PartOut
from common.database.schemas.part import PartCreate, PartUpdate

router = APIRouter(prefix="/parts", tags=["parts"])


@router.get("", response_model=list[PartOut])
async def get_parts(
    part_crud: PartCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await part_crud.get_multi(skip=skip, limit=limit)


@router.get("/{part_id}", response_model=PartOut)
async def get_part(part: PartDep):
    return part


@router.post("", response_model=PartOut, status_code=status.HTTP_201_CREATED)
async def create_part(
    part_in: CreatePartIn,
    part_crud: PartCRUDDep
):
    part_create = PartCreate(**part_in.model_dump())
    return await part_crud.create(obj_in=part_create)


@router.put("/{part_id}", response_model=PartOut)
async def update_part(
    part: PartDep,
    part_in: UpdatePartIn,
    part_crud: PartCRUDDep
):
    part_update = PartUpdate(**part_in.model_dump(exclude_unset=True))
    return await part_crud.update(db_obj=part, obj_in=part_update)


@router.delete("/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_part(part: PartDep, part_crud: PartCRUDDep):
    await part_crud.remove(id=part.id) 
    