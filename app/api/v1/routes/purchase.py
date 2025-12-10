from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.purchase import BuyProductRequest
from app.services.purchase_service import buy_product_service
from app.core.database import get_db
from pydantic import ValidationError
import json

router = APIRouter()

@router.post("/")
async def buy_product(
    product: str = Form(...),
    BILL: str = Form(...),
    COIN: str = Form(...),
):
    try:
        # Convert string → JSON
        product_data = json.loads(product)
        bill_data = json.loads(BILL)
        coin_data = json.loads(COIN)

        # Validate using Pydantic
        data = BuyProductRequest(
            product=product_data,
            BILL=bill_data,
            COIN=coin_data
        )

    except ValidationError as e:
        print(e.json())
        print("\r\n-------log:tag:e.json",e.json(), "\r\n")
        return {
            "status": False,
            "message": "Validation failed",
            "errors": json.loads(e.json())
        }

    # Everything ok → call service
    return await buy_product_service(data)
