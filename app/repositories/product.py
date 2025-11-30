from app.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.future import select
from typing import Optional
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.helpers import uploadFile


# GET ALL PRODUCTS
async def get_all_products(
    db: AsyncSession = Depends(get_db)
) -> list[Product]:
    result = await db.execute(
        select(Product)
        .where(
            Product.is_active.is_(True),
            Product.deleted_at.is_(None)
        ).order_by(Product.id.desc())
    )
    return result.scalars().all()

async def get_product_by_id(
    product_id: int, 
    db: AsyncSession = Depends(get_db)
) -> Optional[Product]:
    result = await db.execute(
        select(Product)
        .where(
            Product.id == product_id,
            Product.is_active.is_(True),
            Product.deleted_at.is_(None)
        )
    )
    return result.scalars().first()

async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    resUploadFile = {'status': False, 'data': None}
    if product_data.image is not None:
        resUploadFile = uploadFile(product_data.image, "products")
        
    new_product = Product(
        title=product_data.title,
        price=product_data.price,
        stock=product_data.stock,
        image=resUploadFile['data'],
        sku=product_data.sku,
        is_active=product_data.is_active
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def update_product(
    product_id: int,
    req: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
    )
    product = result.scalars().first()
    
    resUploadFile = {'status': False, 'data': None}
    if req.image is not None:
        resUploadFile = uploadFile(req.image, "products")
        product.image = resUploadFile['data']
        
    product.title = req.title
    product.price = req.price
    product.stock = req.stock
    product.sku = req.sku

    await db.commit()
    await db.refresh(product)

    return product

async def update_stock_product(
    product_id: int,
    quantity: int,
    is_deduct: bool,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
    )
    product = result.scalars().first()
    if is_deduct == True:
        product.stock -= quantity
    else: 
        product.stock += quantity

    await db.commit()
    await db.refresh(product)

    return product
        
