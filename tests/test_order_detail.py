# tests/test_order_detail.py
import pytest
from unittest.mock import AsyncMock, patch
from types import SimpleNamespace
from app.repositories.order_detail import create_order_detail
from app.schemas.order_detail import OrderDetailCreate

@pytest.fixture
def mock_db():
    from sqlalchemy.ext.asyncio import AsyncSession
    return AsyncMock(spec=AsyncSession)

@pytest.mark.asyncio
async def test_create_order_detail_success(mock_db):
    # arrange
    order_detail_req = OrderDetailCreate(
        order_id=1,
        product_id=2,
        quantity=3,
        total_price=300
    )

    # mock OrderDetail model
    with patch("app.repositories.order_detail.OrderDetail") as MockOrderDetail:
        mock_order_detail_instance = SimpleNamespace(
            order_id=1,
            product_id=2,
            quantity=3,
            total_price=300
        )
        MockOrderDetail.return_value = mock_order_detail_instance

        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # act
        result = await create_order_detail(order_detail_req, mock_db)

        # assert
        mock_db.add.assert_called_once_with(mock_order_detail_instance)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_order_detail_instance)

        assert result == mock_order_detail_instance
        assert result.total_price == 300
        assert result.quantity == 3
