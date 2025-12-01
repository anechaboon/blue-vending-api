from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Column, DateTime
from app.core.database import Base
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
