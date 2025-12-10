from app.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.future import select
from typing import Optional
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.helpers import uploadFile
from datetime import datetime
from app.schemas.base import ErrorResponse

from firebase import db
from datetime import datetime
from fastapi import HTTPException


# GET ALL PRODUCTS
async def get_all_products() -> list[Product]:
    ref = db.collection("product").where("deleted_at", "==", None)
    docs = ref.stream()
    return [
        {**doc.to_dict(), "id": doc.id}
        for doc in docs
    ]

async def get_product_by_id(
    product_id: str
) -> Optional[Product]:
    ref = db.collection("product").document(product_id)
    doc = ref.get()
    if not doc.exists:
        return None
    return {**doc.to_dict(), "id": doc.id}

async def create_product(
    product_data: ProductCreate,
):
    resUploadFile = {'status': False, 'data': None}
    if product_data.image is not None:
        resUploadFile = uploadFile(product_data.image, "products")
    data = {
        "title": product_data.title,
        "price": product_data.price,
        "stock": product_data.stock,
        "sku": product_data.sku,
        "image": resUploadFile['data'],
        "is_active": product_data.is_active,
        "deleted_at": None,
        "created_at": datetime.utcnow()
    }

    # เพิ่ม document ใหม่แบบ auto-id
    doc_ref = db.collection("product").document()
    doc_ref.set(data)

    # ดึงข้อมูลกลับมา (คล้าย refresh)
    doc = doc_ref.get()
    return {**doc.to_dict(), "id": doc.id}

async def update_product(
    product_id: str,
    req: ProductUpdate
):
    ref = db.collection("product").document(str(product_id))
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Product not found")

    resUploadFile = {'status': False, 'data': None}
    if req.image is not None:
        resUploadFile = uploadFile(req.image, "products")

    data = {
        "title": req.title,
        "price": req.price,
        "stock": req.stock,
        "sku": req.sku,
        "is_active": req.is_active,
        "updated_at": datetime.utcnow()
    }

    if resUploadFile['data'] is not None:
        data["image"] = resUploadFile['data']

    ref.update(data)

    # ดึงข้อมูลกลับมา (คล้าย refresh)
    updated_doc = ref.get()
    return {**updated_doc.to_dict(), "id": updated_doc.id}

async def update_stock_product(
    product_id: str,
    quantity: int,
    is_deduct: bool
):
    ref = db.collection("product").document(product_id)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = doc.to_dict()
    current_stock = product_data.get("stock", 0)

    if is_deduct:
        new_stock = max(0, current_stock - quantity)
    else:
        new_stock = current_stock + quantity

    ref.update({
        "stock": new_stock,
        "updated_at": datetime.utcnow()
    })

    # ดึงข้อมูลกลับมา (คล้าย refresh)
    updated_doc = ref.get()
    return {**updated_doc.to_dict(), "id": updated_doc.id}
        
        
async def soft_delete_product(
    product_id: str
):
    ref = db.collection("product").document(product_id)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Product not found")

    ref.update({
        "deleted_at": datetime.utcnow()
    })

    # ดึงข้อมูลกลับมา (คล้าย refresh)
    updated_doc = ref.get()
    return {**updated_doc.to_dict(), "id": updated_doc.id}