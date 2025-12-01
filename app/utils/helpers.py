from fastapi import UploadFile, File, Form
import uuid
import os
import shutil
from app.repositories.cash import get_all_cash
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cash import CashType, Cash

async def calculate_change(cashes: list[Cash], amount_paid: float, total_price: float, db: AsyncSession):
    changeAmount = round(amount_paid - total_price, 2)
    if changeAmount < 0:
        return {
            "status": False,
            "message": "Insufficient payment"
        }  # Not enough payment

    billsStock = {}
    coinsStock = {}
    
    billsChange = {}
    coinsChange = {}
    
    BILL = {}
    COIN = {}
    for cash in cashes:
        cash_dict = cash.__dict__
        if cash_dict['cash'] == 1000:
            continue  # Skip 1000 bills for change
        if cash_dict['cash_type'] == CashType.BILL:
            billsStock[cash_dict['cash']] = 0
            billsChange[cash_dict['cash']] = 0
            BILL[str(cash_dict['cash'])] = 0
        elif cash_dict['cash_type'] == CashType.COIN:
            coinsStock[cash_dict['cash']] = 0
            coinsChange[cash_dict['cash']] = 0
            COIN[str(cash_dict['cash'])] = 0
    
    
    allCash = await get_all_cash(db, None)  # Need to pass db or call from route
    for c in allCash:
        cash = c.__dict__
        if cash['cash'] == 1000:
            continue  # Skip 1000 bills for change
        if cash['cash_type'] == CashType.BILL:
            billsStock[cash['cash']] += cash['stock']
        elif c.cash_type == CashType.COIN:
            coinsStock[cash['cash']] += cash['stock']
    
    for [key, stock] in billsStock.items():
        while changeAmount >= key and stock > 0:
            billsChange[key] += 1
            changeAmount = round(changeAmount - key, 2)
            stock -= 1

    for [key, stock] in coinsStock.items():
        while changeAmount >= key and stock > 0:
            coinsChange[key] += 1
            changeAmount = round(changeAmount - key, 2)
            stock -= 1

    if changeAmount > 0:
        # Not enough change available
        return {
            "status": False,
            "message": "Insufficient change available"
        }  
    
    for [key, qty] in billsChange.items():
        BILL[str(key)] = qty
    for [key, qty] in coinsChange.items():
        COIN[str(key)] = qty
        
    return {
        "status": True,
        "BILL": BILL,
        "COIN": COIN
    }
    
async def prepare_req_update_cashes_stock(
    change_dict: dict,
    is_deduct: bool = True
) -> list[dict]:
    cash_updates = []
    for bill_value, qty in change_dict['BILL'].items():
        if qty > 0:
            cash_updates.append({
                "cash_type": "BILL",
                "cash_value": int(bill_value),
                "quantity": qty,
                "is_deduct": is_deduct
            })
    for coin_value, qty in change_dict['COIN'].items():
        if qty > 0:
            cash_updates.append({
                "cash_type": "COIN",
                "cash_value": int(coin_value),
                "quantity": qty,
                "is_deduct": is_deduct
            })
    return cash_updates

BASE_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
def uploadFile(file: UploadFile, destination_folder: str) -> dict:
    try: 
        if file is not None:
            file.file.seek(0)
            
            file_extension = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{file_extension}"
            
            upload_dir = os.path.join(BASE_UPLOAD_DIR, destination_folder)
            os.makedirs(upload_dir, exist_ok=True)

            file_location = os.path.join(upload_dir, filename)

            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            return {
                'data': filename,
                'message': 'File uploaded successfully',
                'status': True,
            }
    except Exception as e:
        return {
            'data': None,
            'message': f'File upload failed: {str(e)}',
            'status': False,
        }
        
    return {
        'data': None,
        'message': 'No file provided',
        'status': False,
    }