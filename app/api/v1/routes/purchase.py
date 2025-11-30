from fastapi import APIRouter
from app.schemas.purchase import BuyProductRequest
from app.services.purchase_service import buy_product_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Form
from app.core.database import get_db
import json

router = APIRouter()

@router.post("/")
async def buy_product(
    product: str = Form(...),
    bill: str = Form(...),
    coin: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Convert string → JSON
    data = BuyProductRequest(
        product=json.loads(product),
        bill=json.loads(bill),
        coin=json.loads(coin)
    )
    return await buy_product_service(data, db)

    
