from app.schemas.purchase import BuyProductRequest, BuyProductResponse
from app.repositories.product import get_product_by_id
from app.repositories.cash import update_cashes_stock
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helpers import calculate_change, prepare_req_update_cashes_stock

class ProductNotFound(Exception):
    pass

async def buy_product_service(
    data: BuyProductRequest,
    db: AsyncSession
) -> BuyProductResponse:

    totalPaid = (
        data.bill.b20 * 20 +
        data.bill.b50 * 50 +
        data.bill.b100 * 100 +
        data.bill.b500 * 500 +
        data.bill.b1000 * 1000 +
        data.coin.c1 * 1 +
        data.coin.c2 * 2 +
        data.coin.c5 * 5 +
        data.coin.c10 * 10
    )
    
    resProduct = await get_product_by_id(data.product_id, db)
    totalAmount = resProduct.price * data.quantity
    if not resProduct:
        raise ProductNotFound(f"Product with id {data.product_id} not found.")
    if totalPaid < totalAmount:
        raise ProductNotFound(f"Insufficient funds to buy {resProduct.title}.")
    if resProduct.stock < data.quantity:
        raise ProductNotFound(f"Insufficient stock for {resProduct.title}.")
    
    # Update cash stock being paid
    reqUpdateCashStock = {
        "bill": {
            "20": data.bill.b20,
            "50": data.bill.b50,
            "100": data.bill.b100,
            "500": data.bill.b500,
            "1000": data.bill.b1000,
        },
        "coin": {
            "1": data.coin.c1,
            "2": data.coin.c2,
            "5": data.coin.c5,
            "10": data.coin.c10,
        }
    }
    cash_updates = await prepare_req_update_cashes_stock(reqUpdateCashStock, is_deduct=False)  
    await update_cashes_stock(cash_updates, db) 
    
    resChange = await calculate_change(totalPaid, totalAmount, db)
    if resChange['status'] == False:
        raise ProductNotFound(resChange['message'])
    
    # Update cash stock exchanged
    cash_updates = await prepare_req_update_cashes_stock(resChange, is_deduct=True)  
    await update_cashes_stock(cash_updates, db) 
    
    # Deduct product stock
    resProduct.stock -= data.quantity
    await db.commit()
    await db.refresh(resProduct)

    return {
        "product_id": resProduct.id,
        "quantity": data.quantity,
        "total_price": data.quantity * resProduct.price,
        "change_bill": resChange['bill'],
        "change_coin": resChange['coin'],
        "status": True
    }

