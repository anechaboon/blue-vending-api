from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from app.schemas.base import BaseResponse

class UpdateStockRequest(BaseModel):
    cash_id: Optional[int] = None
    cash_type: Optional[str] = None
    cash_value: Optional[int] = None
    quantity: int
    is_deduct: bool
    
class CashType(str, Enum):
    COIN = "COIN"
    BILL = "BILL"

class CashItem(BaseModel):
    id: int
    cash_type: str
    cash: int
    stock: int
    is_active: bool
    model_config = {"from_attributes": True}  # enable ORM mode
    
class CashResponse(BaseResponse):
    data: CashItem

class CashListResponse(BaseResponse):
    data: List[CashItem]

class CashBase(BaseModel):
    cash_type: str
    cash: int
    stock: int
    is_active: Optional[bool] = True

class CashCreate(CashBase):
    pass

class CashUpdate(CashBase):
    pass

class CashNotFound(Exception):
    pass
