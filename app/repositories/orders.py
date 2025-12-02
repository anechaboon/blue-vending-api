from app.models.orders import Order
from sqlalchemy.ext.asyncio import AsyncSession

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

