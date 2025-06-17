from fastapi import APIRouter, status
from app.dependencies.part_category import PartCategoryCRUDDep, PartCategoryDep
from app.schemas.part_category import CreatePartCategoryIn, UpdatePartCategoryIn, PartCategoryOut
from common.database.schemas.part_category import PartCategoryCreate, PartCategoryUpdate

router = APIRouter(prefix="/part-categories", tags=["part-categories"])


@router.get("", response_model=list[PartCategoryOut])
async def get_part_categories(
    part_category_crud: PartCategoryCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await part_category_crud.get_multi(skip=skip, limit=limit)


@router.get("/{part_category_id}", response_model=PartCategoryOut)
async def get_part_category(part_category: PartCategoryDep):
    return part_category


@router.post("", response_model=PartCategoryOut, status_code=status.HTTP_201_CREATED)
async def create_part_category(
    part_category_in: CreatePartCategoryIn,
    part_category_crud: PartCategoryCRUDDep
):
    part_category_create = PartCategoryCreate(**part_category_in.model_dump())
    return await part_category_crud.create(obj_in=part_category_create)


@router.put("/{part_category_id}", response_model=PartCategoryOut)
async def update_part_category(
    part_category: PartCategoryDep,
    part_category_in: UpdatePartCategoryIn,
    part_category_crud: PartCategoryCRUDDep
):
    part_category_update = PartCategoryUpdate(**part_category_in.model_dump(exclude_unset=True))
    return await part_category_crud.update(db_obj=part_category, obj_in=part_category_update)


@router.delete("/{part_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_part_category(part_category: PartCategoryDep, part_category_crud: PartCategoryCRUDDep):
    await part_category_crud.remove(id=part_category.id) 
    