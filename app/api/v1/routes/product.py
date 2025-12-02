from fastapi import APIRouter, Form, UploadFile, File, Depends
from app.schemas.product import ProductResponse, UpdateStockRequest, ProductListResponse, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.product import create_product, update_stock_product, get_all_products, update_product

router = APIRouter()

# GET ALL PRODUCTS
@router.get("/", response_model=ProductListResponse)
async def get_all(
    db: AsyncSession = Depends(get_db)
):
    resProducts = await get_all_products(db=db)
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
    

@router.post("/", response_model=ProductResponse)
async def create(
    title: str = Form(...),
    price: str = Form(...),
    stock: str = Form(...),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db)
):
    req = ProductUpdate(
        title=title,
        price=price,
        stock=stock,
        image=image
    )
    product = await create_product(req, db=db)
    return {
        "data": product,
        "status": True,
        "message": "Product created successfully"
    }

@router.put("/{product_id}", response_model=ProductResponse)
async def update(
    product_id: int, 
    title: str = Form(...),
    price: str = Form(...),
    stock: str = Form(...),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db)
):
    req = ProductUpdate(
        title=title,
        price=price,
        stock=stock,
        image=image
    )
    product = await update_product(product_id, req, db=db)
    return {
        "data": product,
        "status": True,
        "message": "Product updated successfully"
    }


@router.put("/", response_model=ProductResponse)
async def update_product_stock(
    req: UpdateStockRequest,
    db: AsyncSession = Depends(get_db)
):
    product = await update_stock_product(req.product_id, req.quantity, req.is_deduct, db=db)
    return {
        "data": product,
        "status": True,
        "message": "Stock updated successfully"
    }


