# tests/test_cash.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from types import SimpleNamespace
from app.schemas.cash import CashCreate, CashUpdate, CashNotFound
from app.repositories.cash import (
    get_all_cash,
    create_cash,
    update_cash,
    soft_delete_cash,
    update_stock_cash
)

# ---------------- Helper ----------------
def mock_scalar(result):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = result
    return mock_result

def mock_scalars_all(values):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = values
    return mock_result

# ---------------- Fixtures ----------------
@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def sample_cash_instance():
    return SimpleNamespace(
        id=1,
        cash_type="COIN",
        cash=10,
        stock=100,
        is_active=True,
        deleted_at=None
    )

# ---------------- get_all_cash ----------------
@pytest.mark.asyncio
async def test_get_all_coin_cash_success(mock_db, sample_cash_instance):
    sample_cash_instance.is_active = True
    mock_db.execute.return_value = mock_scalars_all([sample_cash_instance])
    result = await get_all_cash(mock_db, cash_type="COIN", is_active="True")
    assert all(cash.is_active is True for cash in result)
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_bill_cash_success(mock_db, sample_cash_instance):
    sample_cash_instance.is_active = True
    mock_db.execute.return_value = mock_scalars_all([sample_cash_instance])
    result = await get_all_cash(mock_db, cash_type="BILL", is_active="True")
    assert all(cash.is_active is True for cash in result)
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_cash_success(mock_db, sample_cash_instance):
    sample_cash_instance.is_active = True
    mock_db.execute.return_value = mock_scalars_all([sample_cash_instance])
    result = await get_all_cash(mock_db)
    assert all(cash.is_active is True for cash in result)
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_true_cash_success(mock_db, sample_cash_instance):
    sample_cash_instance.is_active = True
    mock_db.execute.return_value = mock_scalars_all([sample_cash_instance])
    result = await get_all_cash(mock_db, cash_type=None, is_active="True")
    assert all(cash.is_active is True for cash in result)
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_false_cash_success(mock_db, sample_cash_instance):
    sample_cash_instance.is_active = False
    mock_db.execute.return_value = mock_scalars_all([sample_cash_instance])
    result = await get_all_cash(mock_db, cash_type=None, is_active="False")
    assert all(cash.is_active is False for cash in result)
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_cash_all_success(mock_db, sample_cash_instance):
    mock_db.execute.return_value = mock_scalars_all([sample_cash_instance])
    result = await get_all_cash(mock_db, cash_type=None, is_active="all")
    assert len(result) == 1
    assert result[0] == sample_cash_instance
    mock_db.execute.assert_called_once()
    
@pytest.mark.asyncio
async def test_get_all_cash_empty(mock_db):
    mock_db.execute.return_value = mock_scalars_all([])
    result = await get_all_cash(mock_db, cash_type=None, is_active="all")
    assert result == []
    mock_db.execute.assert_called_once()
    

# ---------------- create_cash ----------------
@pytest.mark.asyncio
async def test_create_cash_success(mock_db):
    req = CashCreate(cash_type="COIN", cash=10, stock=100, is_active=True)
    with patch("app.repositories.cash.Cash") as MockCash:
        mock_cash_instance = SimpleNamespace()
        MockCash.return_value = mock_cash_instance
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await create_cash(req, mock_db)

        mock_db.add.assert_called_once_with(mock_cash_instance)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_cash_instance)
        assert result == mock_cash_instance
        
@pytest.mark.asyncio
async def test_create_cash_inactive_success(mock_db):
    req = CashCreate(cash_type="BILL", cash=50, stock=50, is_active=False)

    with patch("app.repositories.cash.Cash") as MockCash:
        mock_cash_instance = SimpleNamespace(is_active=req.is_active)
        MockCash.return_value = mock_cash_instance

        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await create_cash(req, mock_db)

        mock_db.add.assert_called_once_with(mock_cash_instance)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_cash_instance)

        assert result == mock_cash_instance
        assert getattr(mock_cash_instance, "is_active", None) is False

@pytest.mark.asyncio
async def test_create_cash_failure(mock_db):
    req = CashCreate(cash_type="COIN", cash=10, stock=100, is_active=True)

    with patch("app.repositories.cash.Cash") as MockCash:
        mock_cash_instance = SimpleNamespace()
        MockCash.return_value = mock_cash_instance

        mock_db.commit = AsyncMock(side_effect=Exception("DB Commit Failed"))
        mock_db.refresh = AsyncMock()

        with pytest.raises(Exception) as exc_info:
            await create_cash(req, mock_db)

        assert str(exc_info.value) == "DB Commit Failed"
        mock_db.add.assert_called_once_with(mock_cash_instance)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_not_called()

# ---------------- update_cash ----------------
@pytest.mark.asyncio
async def test_update_cash_success(mock_db, sample_cash_instance):
    mock_db.execute.return_value = mock_scalar(sample_cash_instance)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    req = CashUpdate(cash_type="COIN", cash=20, stock=200, is_active=True)
    result = await update_cash(1, req, mock_db)

    assert sample_cash_instance.cash == 20
    assert sample_cash_instance.stock == 200
    assert result == sample_cash_instance
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_cash_instance)

@pytest.mark.asyncio
async def test_update_cash_not_found(mock_db):
    mock_db.execute.return_value = mock_scalar(None)
    req = CashUpdate(cash_type="COIN", cash=20, stock=200, is_active=True)
    with pytest.raises(CashNotFound):
        await update_cash(999, req, mock_db)

# ---------------- soft_delete_cash ----------------
@pytest.mark.asyncio
async def test_soft_delete_cash_success(mock_db, sample_cash_instance):
    mock_db.execute.return_value = mock_scalar(sample_cash_instance)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    result = await soft_delete_cash(1, mock_db)

    assert sample_cash_instance.deleted_at is not None
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_cash_instance)

@pytest.mark.asyncio
async def test_soft_delete_cash_not_found(mock_db):
    mock_db.execute.return_value = mock_scalar(None)
    with pytest.raises(CashNotFound):
        await soft_delete_cash(999, mock_db)

# ---------------- update_stock_cash ----------------
@pytest.mark.asyncio
async def test_update_stock_cash_increase(mock_db, sample_cash_instance):
    mock_db.execute.return_value = mock_scalar(sample_cash_instance)
    mock_db.commit = AsyncMock()

    updates = [{"cash_id": 1, "quantity": 10, "is_deduct": False}]
    result = await update_stock_cash(updates, mock_db)

    assert sample_cash_instance.stock == 110
    assert result == [sample_cash_instance]
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_stock_cash_deduct(mock_db, sample_cash_instance):
    mock_db.execute.return_value = mock_scalar(sample_cash_instance)
    mock_db.commit = AsyncMock()

    updates = [{"cash_id": 1, "quantity": 10, "is_deduct": True}]
    result = await update_stock_cash(updates, mock_db)

    assert sample_cash_instance.stock == 90
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_stock_cash_not_found(mock_db):
    mock_db.execute.return_value = mock_scalar(None)
    mock_db.commit = AsyncMock()

    updates = [{"cash_id": 999, "quantity": 10, "is_deduct": False}]
    result = await update_stock_cash(updates, mock_db)

    assert result == []
    mock_db.commit.assert_called_once()
    
@pytest.mark.asyncio
async def test_update_stock_cash_by_type_and_value(mock_db, sample_cash_instance):
    mock_db.execute.return_value = mock_scalar(sample_cash_instance)
    mock_db.commit = AsyncMock()

    updates = [{"cash_type": "COIN", "cash_value": 10, "quantity": 5, "is_deduct": False}]
    result = await update_stock_cash(updates, mock_db)

    assert sample_cash_instance.stock == 105
    assert result == [sample_cash_instance]
    mock_db.commit.assert_called_once()
