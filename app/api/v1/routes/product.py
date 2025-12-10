from fastapi import APIRouter, Form, UploadFile, File, Depends
from app.schemas.product import ProductResponse, UpdateStockRequest, ProductListResponse, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.product import get_product_by_id, create_product, update_stock_product, get_all_products, update_product, soft_delete_product

router = APIRouter()

# GET ALL PRODUCTS
@router.get("/", response_model=ProductListResponse)
async def get_all():
    resProducts = await get_all_products()
    if not resProducts:
        return {
            "data": [],
            "status": True,
            "message": "No products found"
        }
        
    return {
        "data": resProducts,
        "status": True,
        "message": "success"
    }
    
@router.get("/{product_id}", response_model=ProductResponse)
async def get_by_id(
    product_id: str
):
    resProduct = await get_product_by_id(product_id)
    if not resProduct:
        return {
            "data": None,
            "status": False,
            "message": "Product not found"
        }
    return {
        "data": resProduct,
        "status": True,
        "message": "success"
    }
    

@router.post("/", response_model=ProductResponse)
async def create(
    title: str = Form(...),
    price: str = Form(...),
    stock: str = Form(...),
    sku: str = Form(...),
    image: UploadFile | None = File(None),
):
    req = ProductUpdate(
        title=title,
        price=price,
        stock=stock,
        sku=sku,
        image=image
    )
    product = await create_product(req)
    return {
        "data": product,
        "status": True,
        "message": "Product created successfully"
    }

@router.put("/{product_id}", response_model=ProductResponse)
async def update(
    product_id: str, 
    title: str = Form(...),
    price: str = Form(...),
    stock: str = Form(...),
    sku: str = Form(...),
    image: UploadFile | None = File(None)
):
    req = ProductUpdate(
        title=title,
        price=price,
        stock=stock,
        sku=sku,
        image=image
    )
    product = await update_product(product_id, req)
    return {
        "data": product,
        "status": True,
        "message": "Product updated successfully"
    }


@router.put("/", response_model=ProductResponse)
async def update_product_stock(
    req: UpdateStockRequest
):
    product = await update_stock_product(req.product_id, req.quantity, req.is_deduct)
    return {
        "data": product,
        "status": True,
        "message": "Stock updated successfully"
    }


@router.delete("/{product_id}", response_model=ProductResponse)
async def delete_product(
    product_id: str
):

    res = await soft_delete_product(product_id)
    return {
        "data": res,
        "status": True,
        "message": "Cash deleted successfully"
    }    



