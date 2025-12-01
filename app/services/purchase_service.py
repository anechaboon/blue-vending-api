from app.schemas.purchase import BuyProductRequest, BuyProductResponse
from app.repositories.product import get_product_by_id, update_stock_product
from app.repositories.cash import update_stock_cash, get_all_cash
from app.repositories.order import create_order
from app.repositories.order_detail import create_order_detail
from app.schemas.order_detail import OrderDetailCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helpers import calculate_change, prepare_req_update_cashes_stock

class ProductNotFound(Exception):
    pass

async def buy_product_service(
    req: BuyProductRequest,
    db: AsyncSession
) -> BuyProductResponse:

    totalPaid = 0
    reqUpdateCashStock = {}

    cashes = await get_all_cash(db, cash_type=None)

    # calculate total paid amount
    for cash in cashes:
        # convert Enum to string
        section = getattr(req, cash.cash_type.value)  # if cash.cash_type == CashType.BILL → req.BILL
        key = f"{cash.cash_type.value}{cash.cash}" 
        amount = section.get(key, 0)

        totalPaid += amount * cash.cash

        reqUpdateCashStock.setdefault(cash.cash_type.value, {})
        reqUpdateCashStock[cash.cash_type.value][cash.cash] = amount


    totalAmount = 0
    for item in req.product:
        resProduct = await get_product_by_id(item.id, db)
        if not resProduct:
            raise ProductNotFound(f"Product with id {item.id} not found.")
        if resProduct.stock < item.quantity:
            raise ProductNotFound(f"Insufficient stock for {resProduct.title}.")

        totalAmount += resProduct.price * item.quantity


    if totalPaid < totalAmount:
        raise ProductNotFound("Insufficient funds.")

    # update stock cash from paid amount
    cashUpdates = await prepare_req_update_cashes_stock(reqUpdateCashStock, is_deduct=False)
    await update_stock_cash(cashUpdates, db)

    # calculate change
    resChange = await calculate_change(cashes, totalPaid, totalAmount, db)
    if resChange["status"] is False:
        raise ProductNotFound(resChange["message"])

    # update stock cash for change given
    cashUpdates = await prepare_req_update_cashes_stock(resChange, is_deduct=True)
    await update_stock_cash(cashUpdates, db)

    resCreateOrder = await create_order(totalAmount, db)

    # create order details and update product stock
    for product in req.product:
        orderDetailReq = OrderDetailCreate(
            order_id=resCreateOrder.id,
            product_id=product.id,
            quantity=product.quantity,
            total_price=product.quantity * product.price
        )

        res = await create_order_detail(orderDetailReq, db=db)
        if not res:
            raise ProductNotFound("Failed to create order detail")

        # update product stock
        res = await update_stock_product(
            product_id=product.id,
            quantity=product.quantity,
            is_deduct=True,
            db=db
        )

        if not res:
            raise ProductNotFound(f"Failed to update stock for product id {product.id}")

    await db.commit()

    return {
        "total_price": totalAmount,
        "change_bill": resChange["BILL"],
        "change_coin": resChange["COIN"],
        "status": True
    }
