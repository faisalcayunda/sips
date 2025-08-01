import asyncio
import os
import sys

from sqlalchemy.ext.asyncio import create_async_engine

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import os
import sys

from app.core.config import settings
from app.models import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle=3600)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_engine():
    """Properly dispose the engine to prevent connection leaks"""
    await engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(create_tables())
    finally:
        asyncio.run(dispose_engine())
