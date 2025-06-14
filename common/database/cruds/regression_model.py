from common.database.cruds.base import BaseCRUD
from common.database.models.regression_model import RegressionModel
from common.database.schemas.regression_model import RegressionModelCreate, RegressionModelUpdate

class RegressionModelCRUD(BaseCRUD[RegressionModel, RegressionModelCreate, RegressionModelUpdate]):
    model = RegressionModel