import uuid

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from common.database.cruds.base import BaseCRUD
from common.database.models.part import Part
from common.database.models.scraped_part_data import ScrapedPartData
from common.database.schemas.scraped_part_data import ScrapedPartDataCreate, ScrapedPartDataUpdate

class ScrapedPartDataCRUD(BaseCRUD[ScrapedPartData, ScrapedPartDataCreate, ScrapedPartDataUpdate]):
    model = ScrapedPartData
    
    async def get_price_regression_data(self, category_id: uuid.UUID) -> list[ScrapedPartData]:
        query = (
            select(ScrapedPartData)
            .join(Part, Part.id == ScrapedPartData.part_id)
            .where(Part.category_id == category_id)
            .distinct(self.model.platform_id, self.model.article_number)
            .options(
                joinedload(ScrapedPartData.platform)
            )
            .order_by(
                self.model.platform_id,
                self.model.article_number,
                self.model.scraped_at.desc()
            )
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())
