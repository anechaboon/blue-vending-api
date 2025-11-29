# app/core/exception_handlers.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.services.purchase_service import ProductNotFound

async def product_not_found_handler(request: Request, exc: ProductNotFound):
    return JSONResponse(
        status_code=200,
        content={
            "product_id": None,
            "quantity": None,
            "total_price": None,
            "change_bill": None,
            "change_coin": None,
            "status": False,
            "message": str(exc)
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "product_id": None,
            "quantity": None,
            "total_price": None,
            "change_bill": None,
            "change_coin": None,
            "status": False,
            "message": "Internal server error"
        }
    )
