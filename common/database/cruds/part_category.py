from common.database.cruds.base import BaseCRUD
from common.database.models.part_category import PartCategory
from common.database.schemas.part_category import PartCategoryCreate, PartCategoryUpdate

class PartCategoryCRUD(BaseCRUD[PartCategory, PartCategoryCreate, PartCategoryUpdate]):
    model = PartCategory
    