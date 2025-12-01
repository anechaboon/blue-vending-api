from fastapi import APIRouter, Form, APIRouter, Depends
from app.schemas.cash import CashListResponse, CashResponse, UpdateStockRequest, CashUpdate, CashCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.cash import get_all_cash, update_stock_cash, update_cash, soft_delete_cash, create_cash

router = APIRouter()

# GET all cash
@router.get("/", response_model=CashListResponse)
async def get_cashes(
    cash_type: str | None = None,
    is_active: str = 'True',
    db: AsyncSession = Depends(get_db)
):
    cashes = await get_all_cash(db, cash_type=cash_type, is_active=is_active)
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

@router.post("/", response_model=CashResponse)
async def create(
    cash_type: str = Form(...),
    cash: str = Form(...),
    stock: str = Form(...),
    is_active: bool = Form(...),
    db: AsyncSession = Depends(get_db)
):
    req = CashCreate(
        cash_type=cash_type,
        cash=cash,
        stock=stock,
        is_active=is_active
    )
    new_cash = await create_cash(req=req, db=db)
    return {
        "data": new_cash,
        "status": True,
        "message": "Cash created successfully"
    }

@router.put("/{cash_id}", response_model=CashResponse)
async def update(
    cash_id: int, 
    cash_type: str = Form(...),
    cash: str = Form(...),
    stock: str = Form(...),
    is_active: bool = Form(...),
    db: AsyncSession = Depends(get_db)
):

    req = CashUpdate(
        cash_type=cash_type,
        cash=cash,
        stock=stock,
        is_active=is_active
    )
    res = await update_cash(cash_id, req, db=db)
    return {
        "data": res,
        "status": True,
        "message": "Cash updated successfully"
    }
    
@router.delete("/{cash_id}", response_model=CashResponse)
async def delete_cash(
    cash_id: int,
    db: AsyncSession = Depends(get_db)
):

    res = await soft_delete_cash(cash_id, db=db)
    return {
        "data": res,
        "status": True,
        "message": "Cash deleted successfully"
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
    
    updated_records = await update_stock_cash(cash_updates, db=db)
    return {
        "data": updated_records,
        "status": True,
        "message": "Stock updated successfully"
    }

