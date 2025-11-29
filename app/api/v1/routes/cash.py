from fastapi import APIRouter
from app.schemas.cash import CashResponse, CashListResponse

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.cash import Cash
from app.core.database import get_db, engine, Base
from datetime import datetime, timezone

router = APIRouter()

    
# GET all cash
@router.get("/", response_model=CashListResponse)
async def get_cashes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cash)
        .where(Cash.deleted_at == None)
        .order_by(Cash.created_at.desc()))
    
    data = result.scalars().all()
    if not data:
        return {
            "data": None,
            "message": "No cash found",
            "status": False,
        }
    return {
        "data": data,
        "message": "Cash retrieved successfully",
        "status": True,
    }