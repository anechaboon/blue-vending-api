from app.models.product import Product
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_product(db: AsyncSession):
    products = [
        Product(title='Coca-Cola can', sku='CC-001', stock=100, price=18, is_active=True),
        Product(title='Pepsi bottle', sku='PB-002', stock=100, price=35, is_active=True),
        Product(title='Sprite can', sku='SC-003', stock=100, price=17, is_active=True)
    ]

    for a in products:
        result = await db.execute(select(Product).filter_by(title=a.title))
        exists = result.scalar_one_or_none()
        if not exists:
            db.add(a)
    
    await db.commit()
