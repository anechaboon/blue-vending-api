from app.models.order import Order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

async def create_order(
    total_amount: float,
    db: AsyncSession
) -> Order:
    new_order = Order(
        total_amount=total_amount
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

