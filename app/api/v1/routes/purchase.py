from fastapi import APIRouter
from app.schemas.purchase import BuyProductRequest, BuyProductResponse
from app.services.purchase_service import buy_product_service

router = APIRouter()

@router.post("/", response_model=BuyProductResponse)
async def buy_product(data: BuyProductRequest):
    return await buy_product_service(data)
    
