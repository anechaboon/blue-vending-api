from app.schemas.purchase import BuyProductRequest, BuyProductResponse
from app.models.product import Product
from app.models.cash import Cash

async def process_purchase(data: BuyProductRequest) -> BuyProductResponse:
    # ทำ business logic buy product (คุณคิดเอง)
    # เช่น ลด stock, เพิ่ม cash, คำนวณเงินทอน เป็นต้น
    pass
