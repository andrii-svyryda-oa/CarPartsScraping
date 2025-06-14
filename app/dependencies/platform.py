from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.platform import PlatformCRUD
from common.database.models.platform import Platform
import uuid

def get_platform_crud(db: DbDep) -> PlatformCRUD:
    return PlatformCRUD(db)

PlatformCRUDDep = Annotated[PlatformCRUD, Depends(get_platform_crud)]

async def get_platform_by_id(platform_id: uuid.UUID, platform_crud: PlatformCRUDDep) -> Platform:
    platform = await platform_crud.get(platform_id)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    return platform

PlatformDep = Annotated[Platform, Depends(get_platform_by_id)] 