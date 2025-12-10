from app.models.cash import Cash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.cash import CashUpdate, CashCreate, CashNotFound
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy import func
from datetime import datetime
from firebase import db
from datetime import datetime
from fastapi import HTTPException

def get_all_cash(cash_type: str = None, is_active: str = "True") -> list[Cash]:
    try:
        ref = db.collection("cash").where("deleted_at", "==", None)

        query = ref
        if is_active == "True":
            query = query.where("is_active", "==", True)
        elif is_active == "False":
            query = query.where("is_active", "==", False)

        if cash_type:
            query = query.where("cash_type", "==", cash_type)

        query = query.order_by("cash_type").order_by("cash")
        
        docs = query.stream()

        return [
            {**doc.to_dict(), "id": doc.id}
            for doc in docs
        ]

    except Exception as e:
        print("Firestore error:", e)
        return []

async def create_cash(req: CashCreate):
    try:
        data = {
            "cash_type": req.cash_type,
            "cash": req.cash,
            "stock": req.stock,
            "is_active": req.is_active,
            "deleted_at": None,
            "created_at": datetime.utcnow()
        }

        # เพิ่ม document ใหม่แบบ auto-id
        doc_ref = db.collection("cash").document()
        doc_ref.set(data)

        # ดึงข้อมูลกลับมา (คล้าย refresh)
        doc = doc_ref.get()
        return {**doc.to_dict(), "id": doc.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_cash(
    cash_id: str,   # ใช้ string เพราะ Firestore doc id เป็น string
    req: CashUpdate,
):
    doc_ref = db.collection("cash").document(cash_id)
    snapshot = doc_ref.get()

    if not snapshot.exists:
        raise HTTPException(status_code=404, detail="Cash not found")

    update_data = {
        "cash_type": req.cash_type,
        "cash": req.cash,
        "stock": req.stock,
        "is_active": req.is_active,
    }

    doc_ref.update(update_data)

    # อ่านข้อมูลหลังอัปเดตกลับไปให้ client
    updated_doc = doc_ref.get()
    return updated_doc.to_dict() | {"id": doc_ref.id}


async def soft_delete_cash(
    cash_id: str,
):
    doc_ref = db.collection("cash").document(cash_id)
    snapshot = doc_ref.get()
    if not snapshot.exists:
        raise HTTPException(status_code=404, detail="Cash not found")
    doc_ref.update({
        "deleted_at": datetime.utcnow()
    })
    deleted_doc = doc_ref.get()
    return deleted_doc.to_dict() | {"id": doc_ref.id}

async def update_stock_cash(
    cash_updates: list[dict]
):
    try:
        batch = db.batch()

        for update in cash_updates:
            cash_id = update.get("cash_id")
            quantity = update.get("quantity")
            is_deduct = update.get("is_deduct", True)

            doc_ref = db.collection("cash").document(cash_id)
            snapshot = doc_ref.get()

            if not snapshot.exists:
                continue  # ข้ามถ้าไม่พบเอกสาร

            current_stock = snapshot.get("stock") or 0
            new_stock = current_stock - quantity if is_deduct else current_stock + quantity

            batch.update(doc_ref, {"stock": new_stock})

        batch.commit()
        return True

    except Exception as e:
        print("Error updating stock:", e)
        return False

