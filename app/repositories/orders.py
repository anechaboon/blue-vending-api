from app.models.orders import Order
from firebase import db
from datetime import datetime
from fastapi import HTTPException

async def create_order(
    total_amount: float
) -> Order:
    try:
        data = {
            "total_amount": total_amount,
            "created_at": datetime.utcnow()
        }

        # Create a new document with auto-generated ID
        doc_ref = db.collection("orders").document()
        doc_ref.set(data)

        # Retrieve the document to return
        doc = doc_ref.get()
        return {**doc.to_dict(), "id": doc.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

