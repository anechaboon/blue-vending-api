import asyncio

from app.db.database import async_session, engine, Base
from app.seeders.cash import seed_cash
from app.seeders.product import seed_product

import logging

logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.ext.asyncio.engine").setLevel(logging.WARNING)

async def run_seeders():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as db:
        await seed_cash(db)
        await seed_product(db)
        await db.commit()

    print("Seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(run_seeders())