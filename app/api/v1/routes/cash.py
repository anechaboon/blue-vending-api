from fastapi import APIRouter
from app.schemas.cash import CashListResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from fastapi import APIRouter, Depends
from app.repositories.cash import get_all_cash

router = APIRouter()

# GET all cash
@router.get("/", response_model=CashListResponse)
async def get_cashes(db: AsyncSession = Depends(get_db)):
    cashes = await get_all_cash(db)
    return {
        "data": cashes, 
        "message": "success",
        "status": True
    }

