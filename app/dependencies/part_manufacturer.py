from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.part_manufacturer import PartManufacturerCRUD
from common.database.models.part_manufacturer import PartManufacturer
import uuid

def get_part_manufacturer_crud(db: DbDep) -> PartManufacturerCRUD:
    return PartManufacturerCRUD(db)

PartManufacturerCRUDDep = Annotated[PartManufacturerCRUD, Depends(get_part_manufacturer_crud)]

async def get_part_manufacturer_by_id(part_manufacturer_id: uuid.UUID, part_manufacturer_crud: PartManufacturerCRUDDep) -> PartManufacturer:
    part_manufacturer = await part_manufacturer_crud.get(part_manufacturer_id)
    if not part_manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part manufacturer not found"
        )
    return part_manufacturer

PartManufacturerDep = Annotated[PartManufacturer, Depends(get_part_manufacturer_by_id)] 