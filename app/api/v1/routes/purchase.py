from fastapi import APIRouter
from app.schemas.purchase import BuyProductRequest
from app.services.purchase_service import buy_product_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db

router = APIRouter()

@router.post("/")
async def buy_product(
    data: BuyProductRequest,
    db: AsyncSession = Depends(get_db)
):
    return await buy_product_service(data, db)

    
