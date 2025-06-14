from fastapi import APIRouter, status
from app.dependencies.scraped_part_data import ScrapedPartDataCRUDDep, ScrapedPartDataDep
from app.schemas.scraped_part_data import CreateScrapedPartDataIn, UpdateScrapedPartDataIn, ScrapedPartDataOut
from common.database.schemas.scraped_part_data import ScrapedPartDataCreate, ScrapedPartDataUpdate

router = APIRouter(prefix="/scraped-part-data", tags=["scraped-part-data"])

@router.get("/", response_model=list[ScrapedPartDataOut])
async def get_scraped_part_data(
    scraped_part_data_crud: ScrapedPartDataCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await scraped_part_data_crud.get_multi(skip=skip, limit=limit)

@router.get("/{scraped_part_data_id}", response_model=ScrapedPartDataOut)
async def get_scraped_part_data_item(scraped_part_data: ScrapedPartDataDep):
    return scraped_part_data

@router.post("/", response_model=ScrapedPartDataOut, status_code=status.HTTP_201_CREATED)
async def create_scraped_part_data(
    scraped_part_data_in: CreateScrapedPartDataIn,
    scraped_part_data_crud: ScrapedPartDataCRUDDep
):
    scraped_part_data_create = ScrapedPartDataCreate(**scraped_part_data_in.model_dump())
    return await scraped_part_data_crud.create(obj_in=scraped_part_data_create)

@router.put("/{scraped_part_data_id}", response_model=ScrapedPartDataOut)
async def update_scraped_part_data(
    scraped_part_data: ScrapedPartDataDep,
    scraped_part_data_in: UpdateScrapedPartDataIn,
    scraped_part_data_crud: ScrapedPartDataCRUDDep
):
    scraped_part_data_update = ScrapedPartDataUpdate(**scraped_part_data_in.model_dump(exclude_unset=True))
    return await scraped_part_data_crud.update(db_obj=scraped_part_data, obj_in=scraped_part_data_update)

@router.delete("/{scraped_part_data_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scraped_part_data(scraped_part_data: ScrapedPartDataDep, scraped_part_data_crud: ScrapedPartDataCRUDDep):
    await scraped_part_data_crud.remove(id=scraped_part_data.id) 