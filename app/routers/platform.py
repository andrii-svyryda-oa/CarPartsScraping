from fastapi import APIRouter, status
from app.dependencies.platform import PlatformCRUDDep, PlatformDep
from app.schemas.platform import CreatePlatformIn, UpdatePlatformIn, PlatformOut
from common.database.schemas.platform import PlatformCreate, PlatformUpdate

router = APIRouter(prefix="/platforms", tags=["platforms"])


@router.get("", response_model=list[PlatformOut])
async def get_platforms(
    platform_crud: PlatformCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await platform_crud.get_multi(skip=skip, limit=limit)


@router.get("/{platform_id}", response_model=PlatformOut)
async def get_platform(platform: PlatformDep):
    return platform


@router.post("", response_model=PlatformOut, status_code=status.HTTP_201_CREATED)
async def create_platform(
    platform_in: CreatePlatformIn,
    platform_crud: PlatformCRUDDep
):
    platform_create = PlatformCreate(**platform_in.model_dump())
    return await platform_crud.create(obj_in=platform_create)


@router.put("/{platform_id}", response_model=PlatformOut)
async def update_platform(
    platform: PlatformDep,
    platform_in: UpdatePlatformIn,
    platform_crud: PlatformCRUDDep
):
    platform_update = PlatformUpdate(**platform_in.model_dump(exclude_unset=True))
    return await platform_crud.update(db_obj=platform, obj_in=platform_update)
    

@router.delete("/{platform_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_platform(platform: PlatformDep, platform_crud: PlatformCRUDDep):
    await platform_crud.remove(id=platform.id) 