from app.models.order_detail import OrderDetail
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order_detail import OrderDetailCreate

from firebase import db
from datetime import datetime
from fastapi import HTTPException

async def create_order_detail(
    req: OrderDetailCreate
) -> OrderDetail:
    try:
        data = {
            "order_id": req.order_id,
            "product_id": req.product_id,
            "quantity": req.quantity,
            "price": req.price,
            "created_at": datetime.utcnow()
        }

        # Create a new document with auto-generated ID
        doc_ref = db.collection("order_details").document()
        doc_ref.set(data)

        # Retrieve the document to return
        doc = doc_ref.get()
        return {**doc.to_dict(), "id": doc.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

