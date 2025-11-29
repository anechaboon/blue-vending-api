from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class CashType(str, Enum):
    COIN = "COIN"
    BILL = "BILL"

class CashResponse(BaseModel):
    id: int
    cash_type: CashType
    cash: int
    stock: int

    model_config = {
        "from_attributes": True   # สำคัญมาก!
    }

class CashListResponse(BaseModel):
    data: List[CashResponse]
    message: str
    status: bool

class CashBase(BaseModel):
    cash_type: str
    cash: int
    stock: int
    is_active: Optional[bool] = True

class CashCreate(CashBase):
    pass

class CashUpdate(CashBase):
    pass
