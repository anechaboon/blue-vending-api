from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, Column, DateTime
from app.core.database import Base
from datetime import datetime, timezone
from sqlalchemy import Enum as SQLEnum
import enum

def utc_now():
    return datetime.now(timezone.utc)

class CashType(enum.Enum):
        COIN = 'COIN'
        BILL = 'BILL'
        
class Cash(Base):
    __tablename__ = 'cash'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cash_type: Mapped[CashType] = mapped_column(SQLEnum(CashType), nullable=False)
    cash: Mapped[int] = mapped_column(Integer, nullable=True) # (1,5,10,20,50,100,500,1000)
    stock: Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    updated_by = Column(Integer, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(Integer, nullable=True)
