from common.database.cruds.base import BaseCRUD
from common.database.models.part_manufacturer import PartManufacturer
from common.database.schemas.part_manufacturer import PartManufacturerCreate, PartManufacturerUpdate

class PartManufacturerCRUD(BaseCRUD[PartManufacturer, PartManufacturerCreate, PartManufacturerUpdate]):
    model = PartManufacturer