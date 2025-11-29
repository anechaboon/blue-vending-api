from pydantic import BaseModel
from typing import Optional, List

class BaseResponse(BaseModel):
    status: bool = True
    message: str = "success"

class UpdateStockRequest(BaseModel):
    product_id: int
    quantity: int
    is_deduct: bool

class ProductItem(BaseModel):
    id: int
    title: str
    price: float
    stock: int
    is_active: bool

    model_config = {"from_attributes": True}  # enable ORM mode

class ProductResponse(BaseResponse):
    data: ProductItem

class ProductListResponse(BaseResponse):
    data: List[ProductResponse]

class ProductBase(BaseModel):
    title: str
    price: float
    stock: int
    sku: Optional[str] = None
    is_active: Optional[bool] = True
    
class ProductCreate(ProductBase):
    pass
class ProductUpdate(ProductBase):
    pass
