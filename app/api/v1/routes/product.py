from fastapi import APIRouter
from app.schemas.product import ProductResponse, UpdateStockRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db
from app.repositories.product import update_stock

router = APIRouter()

@router.post("/update-stock", response_model=ProductResponse)
async def increase_product_stock(
    req: UpdateStockRequest,
    db: AsyncSession = Depends(get_db)
):
    product = await update_stock(req.product_id, req.quantity, req.is_deduct, db=db)
    return {
        "data": product,
        "status": True,
        "message": "Stock updated successfully"
    }


