from app.schemas.purchase import BuyProductRequest, BuyProductResponse
from app.repositories.purchase import process_purchase

async def buy_product_service(data: BuyProductRequest) -> BuyProductResponse:
    # call repositories layer
    result = await process_purchase(data)
    return result
