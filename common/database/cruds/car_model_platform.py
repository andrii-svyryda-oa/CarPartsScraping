from common.database.cruds.base import BaseCRUD
from common.database.models.car_model_platform import CarModelPlatform
from common.database.schemas.car_model_platform import CarModelPlatformCreate, CarModelPlatformUpdate

class CarModelPlatformCRUD(BaseCRUD[CarModelPlatform, CarModelPlatformCreate, CarModelPlatformUpdate]):
    pass

car_model_platform_crud = CarModelPlatformCRUD(CarModelPlatform) 