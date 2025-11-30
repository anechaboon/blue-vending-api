from fastapi import FastAPI
from app.core.exception_handlers import product_not_found_handler, general_exception_handler
from app.api.v1.routes import api_router
from app.services.purchase_service import ProductNotFound
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
# Serve uploaded files statically from /uploads URL (can be accessed via http://<host>/uploads/...)
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(api_router, prefix="/api/v1")

# Exception Handlers
app.add_exception_handler(ProductNotFound, product_not_found_handler)
app.add_exception_handler(Exception, general_exception_handler)
