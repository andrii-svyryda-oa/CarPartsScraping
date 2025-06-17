from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from itertools import groupby
from operator import itemgetter

from common.database.cruds.part import PartCRUD
from common.database.cruds.part_manufacturer import PartManufacturerCRUD
from common.database.cruds.scraped_part_data import ScrapedPartDataCRUD
from common.database.models.car_model import CarModel
from common.database.models.part_manufacturer import PartManufacturer
from common.database.schemas.part import PartCreate
from common.database.schemas.part_manufacturer import PartManufacturerCreate
from common.database.schemas.scraped_part_data import ScrapedPartDataCreate


async def get_or_create_part_manufacturers(
    db: AsyncSession,
    scraped_names: list[str]
) -> list[PartManufacturer]:
    part_manufacturer_crud = PartManufacturerCRUD(db)
    
    existing_part_manufacturers = await part_manufacturer_crud.get_by_names(scraped_names)
    
    existing_manufacturer_names = {part_manufacturer.name for part_manufacturer in existing_part_manufacturers}
    
    new_manufacturer_names = set(scraped_names) - existing_manufacturer_names
    
    if new_manufacturer_names:
        new_part_manufacturers = [
            PartManufacturerCreate(
                name=name,
                description=""
            )
            for name in new_manufacturer_names
        ]
        new_part_manufacturers = await part_manufacturer_crud.create_many(new_part_manufacturers, commit=False) 

        await db.flush()

        existing_part_manufacturers.extend(new_part_manufacturers)

    return existing_part_manufacturers


async def store_category_results(
    db: AsyncSession,
    category_id: str,
    results: list[dict],
    car_model: CarModel
):
    part_crud = PartCRUD(db)
    scraped_part_data_crud = ScrapedPartDataCRUD(db)
    
    sorted_results = sorted(results, key=itemgetter("article_number"))
    
    grouped_results = [
        (oem_number, list(group))
        for oem_number, group
        in groupby(sorted_results, key=itemgetter("article_number"))
    ]
    
    oem_numbers = [oem_number for oem_number, _ in grouped_results]
    
    existing_parts = await part_crud.get_by_oem_numbers(oem_numbers)
    existing_parts_by_oem_number = {part.oem_number: part for part in existing_parts}
    
    manufacturer_names = [result["seller_name"] for result in results]
    
    manufacturers = await get_or_create_part_manufacturers(db, list(set(manufacturer_names)))

    manufacturer_name2id = {
        manufacturer.name: manufacturer.id 
        for manufacturer 
        in manufacturers
    }
    
    existing_part_ids_in_car = [part.id for part in car_model.parts]
    
    oem_number2part = {}
    
    for oem_number, part_results in grouped_results:
        part_result = part_results[0]

        if oem_number in existing_parts_by_oem_number:
            part = existing_parts_by_oem_number[oem_number]
        else:
            part_create = PartCreate(
                manufacturer_id=manufacturer_name2id[part_result["seller_name"]],
                oem_number=oem_number,
                name=part_result["title_on_platform"],
                category_id=UUID(category_id),
                description=""
            )
            
            part = await part_crud.create(obj_in=part_create, commit=False)
            
        oem_number2part[oem_number] = part
        
    await db.flush()
            
    for oem_number, part_results in grouped_results:
        part = oem_number2part[oem_number]
        
        if part.id not in existing_part_ids_in_car:
            car_model.parts.append(part)
            existing_part_ids_in_car.append(part.id)
        
        for result in part_results:
            scraped_part_data_create = ScrapedPartDataCreate(
                part_id=part.id,
                platform_id=result["platform_id"],
                url=result["url"],
                price=result["price"],
                seller_name=result["seller_name"],
                title_on_platform=result["title_on_platform"],
                article_number=result["article_number"],
                availability_status=result["availability_status"],
                seller_type=result["seller_type"],
                location=result["location"],
                search_position=result["search_position"],
                reviews_count=result["reviews_count"],
                images=result["images"]
            )

            await scraped_part_data_crud.create(obj_in=scraped_part_data_create, commit=False)        
