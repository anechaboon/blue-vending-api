from app.schemas.purchase import BuyProductRequest, BuyProductResponse
from app.repositories.product import get_product_by_id, update_stock_product
from app.repositories.cash import update_stock_cash
from app.repositories.order import create_order
from app.repositories.order_detail import create_order_detail
from app.schemas.order_detail import OrderDetailCreate
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
    
    totalAmount = 0
    for product in data.product:
        resProduct = await get_product_by_id(product.id, db)
        product.price = resProduct.price
        
        totalAmount +=  resProduct.price * product.quantity
        if not resProduct:
            raise ProductNotFound(f"Product with id {product.id} not found.")
        if resProduct.stock < product.quantity:
            raise ProductNotFound(f"Insufficient stock for {resProduct.title}.")
        
    if totalPaid < totalAmount:
        raise ProductNotFound(f"Insufficient funds to buy {resProduct.title}.")
    
    
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
    
    cashUpdates = await prepare_req_update_cashes_stock(reqUpdateCashStock, is_deduct=False)  
    await update_stock_cash(cashUpdates, db) 
    
    resChange = await calculate_change(totalPaid, totalAmount, db)
    if resChange['status'] == False:
        raise ProductNotFound(resChange['message'])
    
    # Update cash stock exchanged
    cashUpdates = await prepare_req_update_cashes_stock(resChange, is_deduct=True)  
    await update_stock_cash(cashUpdates, db) 
    
    resCreateOrder = await create_order(totalAmount, db)

    for product in data.product:
    
        orderDetailReq = OrderDetailCreate(
            order_id=resCreateOrder.id,
            product_id=product.id,
            quantity=product.quantity,
            total_price=product.quantity * product.price
        )
        res = await create_order_detail(
            orderDetailReq,
            db=db
        )
        if not res:
            raise ProductNotFound("Failed to create order detail.")
        
        # Deduct product stock
        res = await update_stock_product(
            product_id=product.id,
            quantity=product.quantity,
            is_deduct=True,
            db=db
        )
        if not res:
            raise ProductNotFound(f"Failed to update stock for product id {product.id}.")
    
    await db.commit()
    await db.refresh(resProduct)

    return {
        "total_price": totalAmount,
        "change_bill": resChange['bill'],
        "change_coin": resChange['coin'],
        "status": True
    }

