from sqlalchemy import select
from sqlalchemy.orm import joinedload
from common.database.cruds.base import BaseCRUD
from common.database.models.car_model import CarModel
from common.database.schemas.car_model import CarModelCreate, CarModelUpdate

class CarModelCRUD(BaseCRUD[CarModel, CarModelCreate, CarModelUpdate]):
    model = CarModel
    
    async def get_with_parts(self, id: str):
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .options(joinedload(self.model.parts))
        )
        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()
