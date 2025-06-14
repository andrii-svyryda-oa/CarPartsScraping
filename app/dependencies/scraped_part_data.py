from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.scraped_part_data import ScrapedPartDataCRUD
from common.database.models.scraped_part_data import ScrapedPartData
import uuid

def get_scraped_part_data_crud(db: DbDep) -> ScrapedPartDataCRUD:
    return ScrapedPartDataCRUD(db)

ScrapedPartDataCRUDDep = Annotated[ScrapedPartDataCRUD, Depends(get_scraped_part_data_crud)]

async def get_scraped_part_data_by_id(scraped_part_data_id: uuid.UUID, scraped_part_data_crud: ScrapedPartDataCRUDDep) -> ScrapedPartData:
    scraped_part_data = await scraped_part_data_crud.get(scraped_part_data_id)
    if not scraped_part_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scraped part data not found"
        )
    return scraped_part_data

ScrapedPartDataDep = Annotated[ScrapedPartData, Depends(get_scraped_part_data_by_id)] 