import asyncio
from pathlib import Path
import sys
import uuid

root_path = Path(__file__).parent.parent

sys.path.insert(0, str(root_path))

from common.database.cruds.car_model import CarModelCRUD
from common.database.cruds.part import PartCRUD
from common.database.schemas.part import PartCreate

from common.database.connection import SessionLocal
import common.database.models # noqa

from sqlalchemy.ext.asyncio import AsyncSession
from common.database.cruds.part_manufacturer import PartManufacturerCRUD
from common.database.schemas.part_manufacturer import PartManufacturerCreate

async def main():
    async with SessionLocal() as db:
        part_crud = PartCRUD(db)
        manufacturer_crud = PartManufacturerCRUD(db)
        car_model_crud = CarModelCRUD(db)
        
        manufacturer = await manufacturer_crud.create(obj_in=PartManufacturerCreate(name="VAG", description="VAG"), commit=False)
        
        await db.flush()
        
        part = await part_crud.create(obj_in=PartCreate(
            manufacturer_id=manufacturer.id,
            oem_number="1234567890",
            name="Test",
            category_id=uuid.UUID("328404b4-7827-49af-8ccd-5fa959a8275a")
        ), commit=False)
        
        await db.flush()

        car_model = await car_model_crud.get_with_parts("06bd5eea-8b2a-468a-a293-64f9be82d99d")

        car_model.parts.append(part)
        
        await db.commit()

asyncio.run(main())