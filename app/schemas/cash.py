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

class CashResponse(BaseModel):
    id: int
    cash_type: CashType
    cash: int
    stock: int
    model_config = {
        "from_attributes": True # Enable ORM mode
    }

class CashListResponse(BaseResponse):
    data: List[CashResponse]

class CashBase(BaseModel):
    cash_type: str
    cash: int
    stock: int
    is_active: Optional[bool] = True

class CashCreate(CashBase):
    pass

class CashUpdate(CashBase):
    pass
