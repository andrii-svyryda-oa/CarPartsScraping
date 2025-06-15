from sqlalchemy import select
from common.database.cruds.base import BaseCRUD
from common.database.models.part import Part
from common.database.schemas.part import PartCreate, PartUpdate

class PartCRUD(BaseCRUD[Part, PartCreate, PartUpdate]):
    model = Part

    async def get_by_oem_numbers(self, oem_numbers: list[str]) -> list[Part]:
        stmt = select(self.model).where(self.model.oem_number.in_(oem_numbers))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
