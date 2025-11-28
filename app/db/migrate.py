import asyncio
from app.db.database import Base, engine

async def run_migrate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(run_migrate())
