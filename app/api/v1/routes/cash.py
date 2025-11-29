from fastapi import APIRouter
from app.schemas.cash import CashListResponse, CashResponse, UpdateStockRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from fastapi import APIRouter, Depends
from app.repositories.cash import get_all_cash, update_stock

router = APIRouter()

# GET all cash
@router.get("/", response_model=CashListResponse)
async def get_cashes(db: AsyncSession = Depends(get_db)):
    cashes = await get_all_cash(db)
    if not cashes:
        return {
            "data": [],
            "message": "No cash records found.",
            "status": False
        }
    return {
        "data": cashes, 
        "message": "Cashes retrieved successfully.",
        "status": True
    }

    
@router.post("/update-stock", response_model=CashListResponse)
async def update_cash_stock(
    req: UpdateStockRequest,
    db: AsyncSession = Depends(get_db)
):
    cash_updates = [{
        "quantity": req.quantity,
        "is_deduct": req.is_deduct
    }]
    
    if req.cash_id is not None:
        cash_updates[0]["cash_id"] = req.cash_id
    if req.cash_type is not None and req.cash_value is not None:
        cash_updates[0]["cash_type"] = req.cash_type
        cash_updates[0]["cash_value"] = req.cash_value
    
    updated_records = await update_stock(cash_updates, db=db)
    return {
        "data": updated_records,
        "status": True,
        "message": "Stock updated successfully"
    }

