from fastapi import FastAPI
from app.core.exception_handlers import product_not_found_handler, general_exception_handler
from app.api.v1.routes import api_router
from app.services.purchase_service import ProductNotFound


app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

# Exception Handlers
app.add_exception_handler(ProductNotFound, product_not_found_handler)
app.add_exception_handler(Exception, general_exception_handler)
