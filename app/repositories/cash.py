from app.models.cash import Cash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.cash import CashUpdate
from fastapi import Depends
from app.core.database import get_db

async def get_all_cash(db: AsyncSession) -> list[Cash]:
    result = await db.execute(
        select(Cash)
        .where(Cash.is_active.is_(True), Cash.deleted_at.is_(None))
        .order_by(Cash.created_at.desc())
    )
    return result.scalars().all()

async def update_cash(
    cash_id: int,
    req: CashUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Cash)
        .where(Cash.id == cash_id)
    )
    cash = result.scalars().first()
    cash.cash_type = req.cash_type
    cash.cash = req.cash
    cash.stock = req.stock

    await db.commit()
    await db.refresh(cash)

    return cash

async def update_stock_cash(
    cash_updates: list[dict],
    db: AsyncSession
):
    updated_records = []
    for update in cash_updates:
        stmt = (
            select(Cash)
            .where(
                Cash.is_active.is_(True),
                Cash.deleted_at.is_(None)
            )
        )
        
        if 'cash_id' in update:
            stmt = stmt.where(Cash.id == update['cash_id'])
        elif 'cash_type' in update and 'cash_value' in update:
            stmt = stmt.where(Cash.cash_type == update['cash_type'], Cash.cash == update['cash_value'])
            
        result = await db.execute(stmt)
        cash_record = result.scalars().first()
        if cash_record:
            if update['is_deduct']:
                cash_record.stock -= update['quantity']
            else:
                cash_record.stock += update['quantity']
            db.add(cash_record)
            updated_records.append(cash_record)

    await db.commit()
    return updated_records

