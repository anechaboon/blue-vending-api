from app.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.future import select
from typing import Optional

async def get_product_by_id(
    product_id: int, 
    db: AsyncSession = Depends(get_db)
) -> Optional[Product]:
    result = await db.execute(
        select(Product)
        .where(
            Product.id == product_id,
            Product.is_active.is_(True),
            Product.deleted_at.is_(None)
        )
    )
    return result.scalars().first()