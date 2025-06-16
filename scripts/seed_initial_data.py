import asyncio
import datetime
from pathlib import Path
import sys

root_path = Path(__file__).parent.parent

sys.path.insert(0, str(root_path))

from common.database.cruds.car_brand import CarBrandCRUD
from common.database.cruds.car_model import CarModelCRUD
from common.database.cruds.car_model_platform import CarModelPlatformCRUD
from common.database.cruds.part_category import PartCategoryCRUD
from common.database.cruds.platform import PlatformCRUD
from common.database.schemas.car_brand import CarBrandCreate
from common.database.schemas.car_model import CarModelCreate
from common.database.schemas.car_model_platform import CarModelPlatformCreate
from common.database.schemas.part_category import PartCategoryCreate
from common.database.schemas.platform import PlatformCreate

from common.database.connection import SessionLocal
import common.database.models # noqa

from sqlalchemy.ext.asyncio import AsyncSession
from common.database.cruds.part_manufacturer import PartManufacturerCRUD
from common.database.schemas.part_manufacturer import PartManufacturerCreate


async def seed_base_data_with_exist(db: AsyncSession):
    car_brand_crud = CarBrandCRUD(db)
    car_model_crud = CarModelCRUD(db)
    car_model_platform_crud = CarModelPlatformCRUD(db)
    part_category_crud = PartCategoryCRUD(db)
    platform_crud = PlatformCRUD(db)
    
    car_brand = await car_brand_crud.create(obj_in=CarBrandCreate(
        name="Volkswagen", 
        country_origin="Germany"
    ), commit=False)

    platform = await platform_crud.create(obj_in=PlatformCreate(
        name="Exist", 
        base_url="https://exist.ua", 
        search_url_template="https://exist.ua/uk/volkswagen-cars/golf-vii-5g1-be1-13954/modif-60377/"
    ), commit=False)
    
    await db.flush()
    
    car_model = await car_model_crud.create(obj_in=CarModelCreate(
        name="Golf 7", 
        brand_id=car_brand.id, 
        year_from=datetime.datetime(2013, 1, 1), 
        year_to=datetime.datetime(2023, 1, 1), 
        body_type="Sedan"
    ), commit=False)
    
    await db.flush()
    
    await part_category_crud.create(obj_in=PartCategoryCreate(
        name="Двірники",
        possible_names=["Двірник", "Двірники"],
        description="Двірники"
    ), commit=False)
    
    await car_model_platform_crud.create(obj_in=CarModelPlatformCreate(
        car_model_id=car_model.id, 
        platform_id=platform.id, 
        platform_url="https://exist.ua/uk/volkswagen-cars/golf-vii-5g1-be1-13954/modif-60377/"
    ), commit=False)

    
async def seed_ria_data(db: AsyncSession):
    car_model_crud = CarModelCRUD(db)
    car_model_platform_crud = CarModelPlatformCRUD(db)
    platform_crud = PlatformCRUD(db)
    
    car_models = await car_model_crud.get_multi()
    
    car_model = car_models[0]
    
    platform = await platform_crud.create(obj_in=PlatformCreate(
        name="RIA",
        base_url="https://zapchasti.ria.com",
        search_url_template="https://zapchasti.ria.com/uk/c/zapchasti/?search_text="
    ), commit=False)
    
    await db.flush()
    
    await car_model_platform_crud.create(obj_in=CarModelPlatformCreate(
        car_model_id=car_model.id,
        platform_id=platform.id,
        platform_url="https://zapchasti.ria.com/uk/car/101041/c/legkovye/"
    ), commit=False)

    
async def main():
    async with SessionLocal() as db:
        # await seed_base_data_with_exist(db)
        await seed_ria_data(db)
        await db.commit()


asyncio.run(main())
