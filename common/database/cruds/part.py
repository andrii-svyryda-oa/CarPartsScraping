from common.database.cruds.base import BaseCRUD
from common.database.models.part import Part
from common.database.schemas.part import PartCreate, PartUpdate

class PartCRUD(BaseCRUD[Part, PartCreate, PartUpdate]):
    model = Part