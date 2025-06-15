import asyncio
from celery_apps.io_worker.main import celery_app
from common.database.connection import SessionLocal, async_engine, get_db, get_db_celery
from common.database.cruds.car_brand import CarBrandCRUD

@celery_app.task(name="io.scraping.start")
async def start_scraping():
    async with get_db_celery() as db:
        await asyncio.sleep(4)
        crud = CarBrandCRUD(db)

        car_brands = await crud.get_multi(limit=10)
        
        for car_brand in car_brands:
            print(car_brand.name)

