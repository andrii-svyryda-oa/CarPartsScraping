from common.database.cruds.base import BaseCRUD
from common.database.models.scraped_part_data import ScrapedPartData
from common.database.schemas.scraped_part_data import ScrapedPartDataCreate, ScrapedPartDataUpdate

class ScrapedPartDataCRUD(BaseCRUD[ScrapedPartData, ScrapedPartDataCreate, ScrapedPartDataUpdate]):
    model = ScrapedPartData