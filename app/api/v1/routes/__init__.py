from fastapi import APIRouter

from .cash import router as cash_router
api_router = APIRouter()

api_router.include_router(cash_router, prefix="/cash", tags=["Cash"])
