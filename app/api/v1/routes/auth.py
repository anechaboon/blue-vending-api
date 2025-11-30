# /app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

# นำเข้าสิ่งที่จำเป็น
from app.core.database import get_db
from app.schemas.token import Token # Pydantic Schema สำหรับ Token Response
from app.utils.auth import  create_access_token
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()


# ตั้งค่าเวลาหมดอายุของ Token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login") # not authenticated just to get token
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint to get access token without authentication.
    For development/testing purposes only.
    """
    # Create access token with the provided username
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/validate")
async def validate_token(token: str = Cookie(None)):
    from jose import jwt, JWTError
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM = "HS256"
    
    if not token:
        raise HTTPException(status_code=401, detail="No token")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"email": payload.get("sub")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
@router.post("/logout")
async def logout(response: Response):
    return {"status": True, "message": "Logout successful"}
