from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile, File
from app.schemas.base import BaseResponse

class ProductItem(BaseModel):
    id: str
    title: str
    price: float
    stock: int
    is_active: bool
    sku: Optional[str] = None
    image: Optional[str] = None
    model_config = {"from_attributes": True}  # enable ORM mode

class ProductResponse(BaseResponse):
    data: ProductItem

class ProductListResponse(BaseResponse):
    data: List[ProductItem]
    
class UpdateStockRequest(BaseModel):
    product_id: str
    quantity: int
    is_deduct: bool

class ProductBase(BaseModel):
    title: str
    price: float
    stock: int
    sku: Optional[str] = None
    image: UploadFile | None = File(None),
    is_active: Optional[bool] = True
    
class ProductCreate(ProductBase):
    pass
class ProductUpdate(ProductBase):
    pass
