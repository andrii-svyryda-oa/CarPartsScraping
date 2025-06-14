from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.part_category import PartCategoryCRUD
from common.database.models.part_category import PartCategory
import uuid

def get_part_category_crud(db: DbDep) -> PartCategoryCRUD:
    return PartCategoryCRUD(db)

PartCategoryCRUDDep = Annotated[PartCategoryCRUD, Depends(get_part_category_crud)]

async def get_part_category_by_id(part_category_id: uuid.UUID, part_category_crud: PartCategoryCRUDDep) -> PartCategory:
    part_category = await part_category_crud.get(part_category_id)
    if not part_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part category not found"
        )
    return part_category

PartCategoryDep = Annotated[PartCategory, Depends(get_part_category_by_id)] 