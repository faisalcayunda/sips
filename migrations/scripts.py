import asyncio
import os
import shutil

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def drop_alembic_version_table():
    engine = create_async_engine(os.getenv("DATABASE_URL"))
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))


def migrate():
    os.system("alembic revision --autogenerate -m 'auto generated migration'")
    os.system("alembic upgrade head")


if __name__ == "__main__":
    version_folder = "migrations/versions"
    if not os.path.exists(version_folder):
        os.mkdir(version_folder)
    try:
        asyncio.run(drop_alembic_version_table())
        migrate()
    finally:
        if os.path.exists(version_folder):
            shutil.rmtree(version_folder)
