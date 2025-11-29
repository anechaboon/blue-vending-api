# app/schemas/base.py
from pydantic import BaseModel

class BaseResponse(BaseModel):
    status: bool = True
    message: str = "success"
