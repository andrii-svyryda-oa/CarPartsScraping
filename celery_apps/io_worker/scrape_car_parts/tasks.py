from collections import defaultdict
from uuid import uuid4

from celery import chain, group
from fastapi.encoders import jsonable_encoder
from celery_apps.io_worker.main import celery_app
from celery_apps.io_worker.scrape_car_parts.utils import store_category_results
from common.database.connection import get_db_celery
from common.database.cruds.car_model import CarModelCRUD
from common.database.cruds.car_model_platform import CarModelPlatformCRUD
from common.database.cruds.part_category import PartCategoryCRUD
from common.services.scraping.parts.resolver import get_scraper
from common.utils.files import read_file_json_data, write_file_json_data


@celery_app.task(name="io.scraping.concat_and_store_results")
async def concat_and_store_results(
    platform_id2category_id2result_paths: dict[str, dict[str, list[str]]],
    car_model_id: str
):
    category_id2results = defaultdict(list)
    
    for platform_id, category_id2result_paths in platform_id2category_id2result_paths.items():
        for category_id, result_paths in category_id2result_paths.items():
            for result_path in result_paths:
                results = read_file_json_data(result_path)
                
                for result in results:
                    result["platform_id"] = platform_id

                category_id2results[category_id].extend(results)
                
    async with get_db_celery() as db:
        car_model_crud = CarModelCRUD(db)
        
        car_model = await car_model_crud.get_with_parts(car_model_id)

        for category_id, results in category_id2results.items():
            await store_category_results(
                db=db,
                category_id=category_id,
                results=results,
                car_model=car_model
            )
            
        await db.commit()


@celery_app.task(name="io.scraping.scrape_single_platform_part")
async def scrape_single_platform_part(
    platform_name: str,
    platform_car_model_url: str, 
    category_names: list[str], 
    pages: int,
    result_path: str
):
    scraper_cls = get_scraper(platform_name=platform_name)

    if not scraper_cls:
        raise ValueError("Scraper not found")

    scraper = scraper_cls(
        platform_url=platform_car_model_url,
        category_names=category_names,
        pages=pages
    )

    scraped_data = scraper()
    
    write_file_json_data([jsonable_encoder(data.model_dump()) for data in scraped_data], result_path)


@celery_app.task(name="io.scraping.start")
async def start_scraping(
    platforms_ids: list[str],
    car_model_id: str,
    category_ids: list[str],
    pages: int
):
    async with get_db_celery() as db:
        car_model_platform_crud = CarModelPlatformCRUD(db)
        category_crud = PartCategoryCRUD(db)

        if not platforms_ids:
            car_model_platforms = await car_model_platform_crud.get_by_car(car_model_id)
        else:
            car_model_platforms = await car_model_platform_crud.get_by_platforms_and_car(platforms_ids, car_model_id)

        if not category_ids:
            categories = await category_crud.get_multi(
                skip=0,
                limit=10
            )
        else:
            categories = await category_crud.get_by_ids(category_ids)
        
    run_id = str(uuid4())
    
    platform_id2category_id2result_paths = defaultdict(lambda: defaultdict(list))
    
    tasks = []
        
    for car_model_platform in car_model_platforms:
        for category in categories:
            platform_id = str(car_model_platform.platform_id)
            category_id = str(category.id)
            result_path = f"{run_id}/{platform_id}/{category_id}.json"
            tasks.append(celery_app.signature(
                "io.scraping.scrape_single_platform_part", 
                kwargs={
                    "platform_name": car_model_platform.platform.name, 
                    "platform_car_model_url": car_model_platform.platform_url, 
                    "category_names": category.possible_names, 
                    "pages": pages, 
                    "result_path": result_path
                }
            ))
            
            platform_id2category_id2result_paths[platform_id][category_id].append(result_path)
            
    scrape_all_group = group(tasks)
    
    concat_and_store_results_task = celery_app.signature(
        "io.scraping.concat_and_store_results",
        kwargs={
            "platform_id2category_id2result_paths": platform_id2category_id2result_paths,
            "car_model_id": car_model_id
        },
        immutable=True
    )

    chain(
        scrape_all_group,
        concat_and_store_results_task
    ).apply_async()
    

@celery_app.task(name="io.scraping.start_all")
async def start_all_scraping():
    async with get_db_celery() as db:
        car_model_crud = CarModelCRUD(db)
        car_models = await car_model_crud.get_multi(
            skip=0,
            limit=10
        )
        
    for car_model in car_models:
        celery_app.signature(
            "io.scraping.start",
            kwargs={
                "platforms_ids": [],
                "car_model_id": car_model.id,
                "category_ids": [],
                "pages": 10
            },
            queue="io_queue"
        ).apply_async()
        
