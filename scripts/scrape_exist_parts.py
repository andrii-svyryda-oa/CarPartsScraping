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

scraper_cls = get_scraper("exist")

if not scraper_cls:
    raise ValueError("Scraper not found")

scraper = scraper_cls(
    platform_url="https://exist.ua/uk/volkswagen-cars/golf-vii-5g1-be1-13954/modif-60377/",
    category="Двірники",
    pages=1
)

async def main():
    scraped_data = await scraper()
    
    json.dump([jsonable_encoder(data.model_dump()) for data in scraped_data], open("scripts/data/scraped_exist_data.json", "w"))

asyncio.run(main())
