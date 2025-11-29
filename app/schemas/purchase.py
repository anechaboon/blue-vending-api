from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    id: int
    quantity: int
    price: Optional[float] = 0.0

class BillSchema(BaseModel):
    b20: int = 0
    b50: int = 0
    b100: int = 0
    b500: int = 0
    b1000: int = 0
    
class CoinSchema(BaseModel):
    c1: int = 0
    c2: int = 0
    c5: int = 0
    c10: int = 0
    
class BuyProductRequest(BaseModel):
    product: List[Product]
    bill: BillSchema
    coin: CoinSchema

class BuyProductResponse(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    change_bill: BillSchema
    change_coin: CoinSchema
    status: str
