from fastapi import APIRouter

from .cash import router as cash_router
from .product import router as product_router
from .purchase import router as purchase_router
from .auth import router as auth_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(cash_router, prefix="/cash", tags=["Cash"])
api_router.include_router(product_router, prefix="/product", tags=["Product"])
api_router.include_router(purchase_router, prefix="/purchase", tags=["Purchase"])
