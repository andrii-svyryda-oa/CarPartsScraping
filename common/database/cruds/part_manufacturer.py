from sqlalchemy import select
from common.database.cruds.base import BaseCRUD
from common.database.models.part_manufacturer import PartManufacturer
from common.database.schemas.part_manufacturer import PartManufacturerCreate, PartManufacturerUpdate

class PartManufacturerCRUD(BaseCRUD[PartManufacturer, PartManufacturerCreate, PartManufacturerUpdate]):
    model = PartManufacturer
    
    async def get_by_names(self, names: list[str]) -> list[PartManufacturer]:
        stmt = select(self.model).where(self.model.name.in_(names))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())