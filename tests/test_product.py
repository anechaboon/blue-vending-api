# tests/test_product.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from types import SimpleNamespace
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    update_stock_product
)
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product import soft_delete_product

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
def sample_product_instance():
    return SimpleNamespace(
        id=1,
        title="Sample Product",
        price=100,
        stock=50,
        sku="SKU001",
        image=None,
        is_active=True,
        deleted_at=None
    )

# ---------------- get_all_products ----------------
@pytest.mark.asyncio
async def test_get_all_products_success(mock_db, sample_product_instance):
    mock_db.execute.return_value = mock_scalars_all([sample_product_instance])
    result = await get_all_products(mock_db)
    assert all(prod.is_active is True for prod in result)
    mock_db.execute.assert_called_once()

# ---------------- get_product_by_id ----------------
@pytest.mark.asyncio
async def test_get_product_by_id_success(mock_db, sample_product_instance):
    mock_db.execute.return_value = mock_scalar(sample_product_instance)
    result = await get_product_by_id(1, mock_db)
    assert result == sample_product_instance
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_product_by_id_not_found(mock_db):
    mock_db.execute.return_value = mock_scalar(None)
    result = await get_product_by_id(999, mock_db)
    assert result is None

# ---------------- create_product ----------------
@pytest.mark.asyncio
async def test_create_product_success(mock_db):
    req = ProductCreate(title="New Product", price=150, stock=10, sku="SKU002", image=None, is_active=True)
    
    with patch("app.repositories.product.Product") as MockProduct:
        mock_product_instance = SimpleNamespace()
        MockProduct.return_value = mock_product_instance
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await create_product(req, mock_db)

        mock_db.add.assert_called_once_with(mock_product_instance)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_product_instance)
        assert result == mock_product_instance

# ---------------- update_product ----------------
@pytest.mark.asyncio
async def test_update_product_success(mock_db, sample_product_instance):
    mock_db.execute.return_value = mock_scalar(sample_product_instance)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    req = ProductUpdate(title="Updated", price=200, stock=60, sku="SKU001U", image=None)
    result = await update_product(1, req, mock_db)

    assert sample_product_instance.title == "Updated"
    assert sample_product_instance.price == 200
    assert sample_product_instance.stock == 60
    assert sample_product_instance.sku == "SKU001U"
    assert result == sample_product_instance
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_product_instance)

# ---------------- update_stock_product ----------------
@pytest.mark.asyncio
async def test_update_stock_product_increase(mock_db, sample_product_instance):
    mock_db.execute.return_value = mock_scalar(sample_product_instance)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    result = await update_stock_product(1, quantity=10, is_deduct=False, db=mock_db)
    assert sample_product_instance.stock == 60
    assert result == sample_product_instance
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_stock_product_deduct(mock_db, sample_product_instance):
    mock_db.execute.return_value = mock_scalar(sample_product_instance)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    result = await update_stock_product(1, quantity=20, is_deduct=True, db=mock_db)
    assert sample_product_instance.stock == 30
    assert result == sample_product_instance
    mock_db.commit.assert_called_once()
    
    
async def test_soft_delete_product_success(mock_db, sample_product_instance):
    mock_db.execute.return_value = mock_scalar(sample_product_instance)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    
    result = await soft_delete_product(1, mock_db)
    
    assert sample_product_instance.deleted_at is not None
    assert result == sample_product_instance
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_product_instance)


@pytest.mark.asyncio
async def test_soft_delete_product_not_found(mock_db):
    mock_db.execute.return_value = mock_scalar(None)
    
    
    with pytest.raises(Exception):
        await soft_delete_product(999, mock_db)

