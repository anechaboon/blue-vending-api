from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Column, DateTime
from app.core.database import Base
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class OrderDetail(Base):
    __tablename__ = 'order_detail'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
