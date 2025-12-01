import asyncio
from app.core.database import Base, engine
from app.models.order_detail import OrderDetail
from app.models.orders import Order
from app.models.product import Product
from app.models.cash import Cash
async def run_migrate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(run_migrate())
