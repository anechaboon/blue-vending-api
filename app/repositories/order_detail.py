from app.models.order_detail import OrderDetail
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order_detail import OrderDetailCreate

async def create_order_detail(
    req: OrderDetailCreate,
    db: AsyncSession
) -> OrderDetail:
    new_order_detail = OrderDetail(
        order_id=req.order_id,
        product_id=req.product_id,
        quantity=req.quantity,
        total_price=req.total_price
    )
    db.add(new_order_detail)
    await db.commit()
    await db.refresh(new_order_detail)
    return new_order_detail

