import contextlib
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from common.settings import settings

async_engine = create_async_engine(settings.DATABASE_URL)

SessionLocal = async_sessionmaker(async_engine)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db

@contextlib.asynccontextmanager
async def get_db_celery() -> AsyncGenerator[AsyncSession, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            await db.close()
        await async_engine.dispose()