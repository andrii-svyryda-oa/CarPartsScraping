import asyncio
import datetime
import json
from pathlib import Path
import sys
import uuid

from fastapi.encoders import jsonable_encoder

root_path = Path(__file__).parent.parent

sys.path.insert(0, str(root_path))


from common.database.models.car_model_platform import CarModelPlatform
from common.database.models.part_category import PartCategory
from common.services.scraping.parts.resolver import get_scraper

scraper_cls = get_scraper("ria")

if not scraper_cls:
    raise ValueError("Scraper not found")

scraper = scraper_cls(
    platform_url="https://zapchasti.ria.com/uk/car/101041/c/legkovye/",
    category_names=["Двірник"],
    pages=1
)

scraped_data = scraper()

json.dump([jsonable_encoder(data.model_dump()) for data in scraped_data], open("scripts/data/scraped_ria_data.json", "w"))
