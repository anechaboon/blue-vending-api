# tests/test_order.py
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from types import SimpleNamespace

from app.repositories.orders import create_order
@pytest.fixture
def mock_db():
    db = AsyncMock(spec=AsyncSession)
    return db

@pytest.mark.asyncio
async def test_create_order_success(mock_db):
    # arrange
    total_amount = 150.0

    # mock Order model
    with patch("app.repositories.orders.Order") as MockOrder:
        # mock instance มี attribute
        mock_order_instance = SimpleNamespace(id=1, total_amount=total_amount)
        MockOrder.return_value = mock_order_instance

        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await create_order(total_amount, mock_db)

        mock_db.add.assert_called_once_with(mock_order_instance)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_order_instance)

        assert result == mock_order_instance
        assert result.total_amount == 150.0
