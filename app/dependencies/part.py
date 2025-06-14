from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.part import PartCRUD
from common.database.models.part import Part
import uuid

def get_part_crud(db: DbDep) -> PartCRUD:
    return PartCRUD(db)

PartCRUDDep = Annotated[PartCRUD, Depends(get_part_crud)]

async def get_part_by_id(part_id: uuid.UUID, part_crud: PartCRUDDep) -> Part:
    part = await part_crud.get(part_id)
    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found"
        )
    return part

PartDep = Annotated[Part, Depends(get_part_by_id)] 