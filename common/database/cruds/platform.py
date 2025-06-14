from common.database.cruds.base import BaseCRUD
from common.database.models.platform import Platform
from common.database.schemas.platform import PlatformCreate, PlatformUpdate

class PlatformCRUD(BaseCRUD[Platform, PlatformCreate, PlatformUpdate]):
    model = Platform