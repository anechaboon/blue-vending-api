from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CashBase(BaseModel):
    cash_type: str
    cash: int
    stock: int
    is_active: Optional[bool] = True

class CashRead(CashBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CashListResponse(BaseModel):
    data: List["CashRead"]
    message: str
    status: bool

class CashResponse(BaseModel):
    data: Optional["CashRead"]
    message: str
    status: bool

class CashCreate(CashBase):
    pass

class CashUpdate(CashBase):
    pass
