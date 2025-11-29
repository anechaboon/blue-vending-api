from app.models.cash import Cash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.cash import CashListResponse

async def get_all_cash(db: AsyncSession) -> list[Cash]:
    result = await db.execute(
        select(Cash)
        .where(Cash.is_active.is_(True), Cash.deleted_at.is_(None))
        .order_by(Cash.created_at.desc())
    )
    return result.scalars().all()


# cash_updates = { cash_type, cash_value, quantity, is_deduct }
async def update_cashes_stock(
    cash_updates: list[dict],
    db: AsyncSession
) -> None:
    for update in cash_updates:
        stmt = (
            select(Cash)
            .where(
                Cash.cash_type == update['cash_type'],
                Cash.cash == update['cash_value'],
                Cash.is_active.is_(True),
                Cash.deleted_at.is_(None)
            )
        )
        result = await db.execute(stmt)
        cash_record = result.scalars().first()
        if cash_record:
            if update['is_deduct']:
                cash_record.stock -= update['quantity']
            else:
                cash_record.stock += update['quantity']
            db.add(cash_record)
    await db.commit()

