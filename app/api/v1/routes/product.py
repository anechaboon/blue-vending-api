from fastapi import APIRouter
from app.schemas.product import ProductResponse, UpdateStockRequest, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db
from app.repositories.product import create_product, update_stock_product

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create(
    req: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    product = await create_product(req, db=db)
    return {
        "data": product,
        "status": True,
        "message": "Product created successfully"
    }
    
@router.put("/", response_model=ProductResponse)
async def update_product_stock(
    req: UpdateStockRequest,
    db: AsyncSession = Depends(get_db)
):
    product = await update_stock_product(req.product_id, req.quantity, req.is_deduct, db=db)
    return {
        "data": product,
        "status": True,
        "message": "Stock updated successfully"
    }


