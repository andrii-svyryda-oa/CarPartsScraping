from common.database.cruds.base import BaseCRUD
from common.database.models.car_brand import CarBrand
from common.database.schemas.car_brand import CarBrandCreate, CarBrandUpdate

class CarBrandCRUD(BaseCRUD[CarBrand, CarBrandCreate, CarBrandUpdate]):
    model = CarBrand
