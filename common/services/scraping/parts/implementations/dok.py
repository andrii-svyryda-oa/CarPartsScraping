from common.services.scraping.parts.base import BasePartScraper, implements_platform_scraper, ScrapedPart
from common.database.models.car_model_platform import CarModelPlatform
from common.database.models.part_category import PartCategory


@implements_platform_scraper("dok")
class DokPartScraper(BasePartScraper):
    def __init__(self, car_model_platform: CarModelPlatform, part_category: PartCategory):
        super().__init__(car_model_platform, part_category)

    async def __call__(self) -> list[ScrapedPart]:
        pass
