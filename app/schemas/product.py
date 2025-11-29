from pydantic import BaseModel
from typing import Optional, List
from app.schemas.base import BaseResponse

class UpdateStockRequest(BaseModel):
    product_id: int
    quantity: int
    is_deduct: bool
    
class ProductItem(BaseModel):
    id: int
    title: str
    stock: int

    model_config = {
        "from_attributes": True
    }

class ProductResponse(BaseResponse):
    data: ProductItem

class ProductListResponse(BaseResponse):
    data: List[ProductResponse]

class ProductBase(BaseModel):
    cash_type: str
    cash: int
    stock: int
    is_active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass
