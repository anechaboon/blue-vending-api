from app.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.future import select
from typing import Optional
from app.schemas.product import ProductCreate


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

async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    
    new_product = Product(
        title=product_data.title,
        price=product_data.price,
        stock=product_data.stock,
        sku=product_data.sku,
        is_active=product_data.is_active
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def update_stock_product(
    product_id: int,
    quantity: int,
    is_deduct: bool,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
    )
    product = result.scalars().first()
    if is_deduct == True:
        product.stock -= quantity
    else: 
        product.stock += quantity

    await db.commit()
    await db.refresh(product)

    return product
        
