from pydantic import BaseModel
from typing import Optional, List

class BaseResponse(BaseModel):
    status: bool = True
    message: str = "success"

class UpdateStockRequest(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    total_price: float

class OrderDetailItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    total_price: float
    model_config = {"from_attributes": True}  # enable ORM mode

class OrderDetailResponse(BaseResponse):
    data: OrderDetailItem

class OrderDetailListResponse(BaseResponse):
    data: List[OrderDetailResponse]

class OrderDetailBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    total_price: float
    
class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(OrderDetailBase):
    pass
