from app.models.cash import Cash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_cash(db: AsyncSession):
    cashes = [
        Cash(cash_type='COIN', cash=1, stock=100, is_active=True),
        Cash(cash_type='COIN', cash=2, stock=100, is_active=True),
        Cash(cash_type='COIN', cash=5, stock=100, is_active=True),
        Cash(cash_type='COIN', cash=10, stock=100, is_active=True),
        Cash(cash_type='BILL', cash=20, stock=100, is_active=True),
        Cash(cash_type='BILL', cash=50, stock=100, is_active=True),
        Cash(cash_type='BILL', cash=100, stock=100, is_active=True),
        Cash(cash_type='BILL', cash=500, stock=100, is_active=True),
        Cash(cash_type='BILL', cash=1000, stock=100, is_active=True),
    ]

    for a in cashes:
        result = await db.execute(select(Cash).filter_by(cash_type=a.cash_type, cash=a.cash))
        exists = result.scalar_one_or_none()
        if not exists:
            db.add(a)
    
    await db.commit()
