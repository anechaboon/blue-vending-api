import pytest
import io
import os
from unittest.mock import AsyncMock, patch
from fastapi import UploadFile
from app.models.cash import Cash, CashType
from app.utils.helpers import calculate_change, prepare_req_update_cashes_stock, uploadFile, BASE_UPLOAD_DIR
from app.repositories.cash import get_all_cash


# ------------------------------
# Test calculate_change
# ------------------------------

@pytest.mark.asyncio
async def test_calculate_change_success():
    cashes = [
        Cash(cash=500, cash_type=CashType.BILL, stock=2),
        Cash(cash=100, cash_type=CashType.BILL, stock=5),
        Cash(cash=25, cash_type=CashType.COIN, stock=10),
    ]

    mock_db = AsyncMock()
    with patch("app.utils.helpers.get_all_cash", new_callable=AsyncMock) as mock_get_all_cash:
        mock_get_all_cash.return_value = cashes  # return list ของ Cash
        result = await calculate_change(cashes, amount_paid=1000, total_price=675, db=mock_db)

    assert result["status"] is True
    assert sum(result["BILL"].values()) > 0 and sum(result["COIN"].values()) > 0


@pytest.mark.asyncio
async def test_calculate_change_insufficient_payment():
    cashes = []
    mock_db = AsyncMock()
    result = await calculate_change(cashes, amount_paid=50, total_price=100, db=mock_db)
    assert result["status"] is False
    assert result["message"] == "Insufficient payment"

@pytest.mark.asyncio
async def test_calculate_change_insufficient_change():
    cashes = [Cash(cash=10, cash_type=CashType.BILL, stock=4)]
    mock_db = AsyncMock()
    with patch("app.utils.helpers.get_all_cash", new_callable=AsyncMock) as mock_get_all_cash:
        mock_get_all_cash.return_value = cashes
        result = await calculate_change(cashes, amount_paid=100, total_price=50, db=mock_db)

    assert result["status"] is False
    assert result["message"] == "Insufficient change available"

# ------------------------------
# Test prepare_req_update_cashes_stock
# ------------------------------
@pytest.mark.asyncio
async def test_prepare_req_update_cashes_stock():
    change_dict = {
        "BILL": {"100": 2, "500": 1},
        "COIN": {"25": 3}
    }
    result = await prepare_req_update_cashes_stock(change_dict)
    assert len(result) == 3
    assert all("cash_type" in item and "quantity" in item for item in result)

# ------------------------------
# Test uploadFile
# ------------------------------
def test_uploadFile_success(tmp_path):
    # Create a dummy file
    file_content = b"Hello World"
    file = UploadFile(filename="test.txt", file=io.BytesIO(file_content))

    # Patch BASE_UPLOAD_DIR to tmp_path
    with patch("app.utils.helpers.BASE_UPLOAD_DIR", tmp_path):
        result = uploadFile(file, "test_folder")

    assert result["status"] is True
    assert os.path.exists(os.path.join(tmp_path, "test_folder", result["data"]))

def test_uploadFile_no_file():
    result = uploadFile(None, "test_folder")
    assert result["status"] is False
    assert result["message"] == "No file provided"

def test_uploadFile_exception(monkeypatch):
    file = UploadFile(filename="test.txt", file=io.BytesIO(b"data"))

    def mock_makedirs(*args, **kwargs):
        raise OSError("Cannot create folder")
    
    monkeypatch.setattr(os, "makedirs", mock_makedirs)
    result = uploadFile(file, "test_folder")
    assert result["status"] is False
    assert "File upload failed" in result["message"]
