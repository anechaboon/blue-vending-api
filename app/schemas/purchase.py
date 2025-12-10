from pydantic import BaseModel
from typing import List, Optional, Dict

class Product(BaseModel):
    id: str
    quantity: int
    price: Optional[float] = 0.0

class ProductItem(BaseModel):
    id: str
    quantity: int
    price: Optional[float] = 0.0
    

class BuyProductRequest(BaseModel):
    product: List[ProductItem]
    BILL: Dict[str, int]
    COIN: Dict[str, int]

class BuyProductResponse(BaseModel):
    product_id: str
    quantity: int
    total_price: float
    change_bill: Dict[str, int]
    change_coin: Dict[str, int]
    status: str
