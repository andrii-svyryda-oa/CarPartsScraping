from common.database.cruds.base import BaseCRUD
from common.database.models.car_model import CarModel
from common.database.schemas.car_model import CarModelCreate, CarModelUpdate

class CarModelCRUD(BaseCRUD[CarModel, CarModelCreate, CarModelUpdate]):
    model = CarModel