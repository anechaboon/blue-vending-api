# tests/test_purchase_service.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from types import SimpleNamespace
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.purchase import BuyProductRequest, ProductItem
from app.services.purchase_service import buy_product_service
from app.schemas.base import ErrorResponse

# ---------------- Helper ----------------
def mock_scalar(result):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = result
    return mock_result

def mock_scalars_all(values):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = values
    return mock_result

@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def buy_request():
    # ผู้ใช้ซื้อ 1 ชิ้น ราคา 100 จ่ายเหรียญ 10 x 10 = 100
    return BuyProductRequest(
        product=[ProductItem(id=1, quantity=1, price=100)],
        COIN={"COIN10": 10},
        BILL={}
    )

@pytest.fixture
def sample_product_instance():
    # สร้าง Product instance mock
    return SimpleNamespace(
        id=1,
        title="Product 1",
        price=100,
        stock=10,
        image=None,
        sku="P001",
        is_active=True,
        deleted_at=None
    )

@pytest.fixture
def sample_cash_instance():
    return SimpleNamespace(
        id=1,
        cash_type=SimpleNamespace(value="COIN"),
        cash=10,
        stock=100,
        is_active=True,
        deleted_at=None
    )

@pytest.fixture
def mock_cashes():
    # สมมติ cash มีเหรียญ 10
    return [SimpleNamespace(cash_type=SimpleNamespace(value="COIN"), cash=10)]

# ---------------- Test buy_product_service ----------------
@pytest.mark.asyncio
async def test_purchase_success(mock_db, buy_request, sample_product_instance, sample_cash_instance):
    # Mock repository functions
    with patch("app.services.purchase_service.get_all_cash", new=AsyncMock(return_value=[sample_cash_instance])), \
        patch("app.services.purchase_service.get_product_by_id", new=AsyncMock(return_value=sample_product_instance)), \
        patch("app.services.purchase_service.update_stock_cash", new=AsyncMock()), \
        patch("app.services.purchase_service.update_stock_product", new=AsyncMock(return_value=sample_product_instance)), \
        patch("app.services.purchase_service.create_order", new=AsyncMock(return_value=SimpleNamespace(id=1))), \
        patch("app.services.purchase_service.create_order_detail", new=AsyncMock(return_value=True)), \
        patch("app.services.purchase_service.prepare_req_update_cashes_stock", new=AsyncMock(return_value=[{"cash_id":1,"quantity":10,"is_deduct":False}])), \
        patch("app.services.purchase_service.calculate_change", new=AsyncMock(return_value={"status": True, "BILL": {}, "COIN": {}})):
        
        result = await buy_product_service(buy_request, mock_db)
        
        assert result["total_price"] == 100
        assert result["status"] is True
        assert result["change_bill"] == {}
        assert result["change_coin"] == {}

@pytest.mark.asyncio
async def test_purchase_product_not_found(mock_db, buy_request):
    # mock get_product_by_id ให้ return None
    with patch("app.services.purchase_service.get_all_cash", new=AsyncMock(return_value=[])), \
        patch("app.services.purchase_service.get_product_by_id", new=AsyncMock(return_value=None)):
        
        with pytest.raises(ErrorResponse):
            await buy_product_service(buy_request, mock_db)

@pytest.mark.asyncio
async def test_purchase_insufficient_funds(mock_db, buy_request, sample_product_instance, sample_cash_instance):
    # mock get_all_cash คืนค่าเงินไม่พอ
    sample_cash_instance.cash = 5  # 5*10=50 < 100
    with patch("app.services.purchase_service.get_all_cash", new=AsyncMock(return_value=[sample_cash_instance])), \
        patch("app.services.purchase_service.get_product_by_id", new=AsyncMock(return_value=sample_product_instance)):
        
        with pytest.raises(ErrorResponse):
            await buy_product_service(buy_request, mock_db)
            
@pytest.mark.asyncio
async def test_purchase_calculate_change_fail(mock_db, buy_request, mock_cashes):
    # mock calculate_change ให้ status=False
    with patch("app.services.purchase_service.get_all_cash", AsyncMock(return_value=mock_cashes)), \
        patch("app.services.purchase_service.get_product_by_id", AsyncMock(return_value=SimpleNamespace(id=1, title="Test", stock=10, price=100))), \
        patch("app.services.purchase_service.prepare_req_update_cashes_stock", AsyncMock(return_value=[])), \
        patch("app.services.purchase_service.update_stock_cash", AsyncMock(return_value=None)), \
        patch("app.services.purchase_service.calculate_change", AsyncMock(return_value={"status": False, "message": "Cannot give change"})):

        with pytest.raises(ErrorResponse) as exc:
            await buy_product_service(buy_request, mock_db)
        assert "Cannot give change" in str(exc.value)
        
@pytest.mark.asyncio
async def test_purchase_no_cash_available(mock_db, buy_request):
    with patch(
        "app.services.purchase_service.get_all_cash",
        AsyncMock(return_value=None)
    ):
        with pytest.raises(ErrorResponse) as exc:
            await buy_product_service(buy_request, mock_db)

        assert "No cash available in the system." in str(exc.value)
        
@pytest.mark.asyncio
async def test_purchase_product_not_found_with_cash(mock_db, buy_request, mock_cashes):
    with patch("app.services.purchase_service.get_all_cash", AsyncMock(return_value=mock_cashes)), \
        patch("app.services.purchase_service.get_product_by_id", AsyncMock(return_value=None)
    ):
        with pytest.raises(ErrorResponse) as exc:
            await buy_product_service(buy_request, mock_db)

        assert "Product with id" in str(exc.value) and "not found" in str(exc.value)
