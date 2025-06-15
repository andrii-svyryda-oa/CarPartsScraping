from sqlalchemy import select
from sqlalchemy.orm import joinedload
from common.database.cruds.base import BaseCRUD
from common.database.models.car_model_platform import CarModelPlatform
from common.database.schemas.car_model_platform import CarModelPlatformCreate, CarModelPlatformUpdate

class CarModelPlatformCRUD(BaseCRUD[CarModelPlatform, CarModelPlatformCreate, CarModelPlatformUpdate]):
    model = CarModelPlatform

    async def get_by_platforms_and_cars(self, platforms_ids: list[str], car_model_id: str) -> list[CarModelPlatform]:
        stmt = (
            select(CarModelPlatform)
            .where(
                CarModelPlatform.platform_id.in_(platforms_ids),
                CarModelPlatform.car_model_id == car_model_id
            )
            .options(joinedload(CarModelPlatform.platform))
        )
        result = await self.db.execute(stmt)
        return list(result.unique().scalars().all())

car_model_platform_crud = CarModelPlatformCRUD(CarModelPlatform) 