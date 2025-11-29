"""create_table_cash

Revision ID: fd8788e38c07
Revises: 
Create Date: 2025-11-29 21:13:29.440386

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd8788e38c07'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # สร้าง ENUM แบบปลอดภัย
    op.execute("""
    DO $$
    BEGIN
        CREATE TYPE cashtype AS ENUM ('COIN', 'BILL');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    """)

    cash_type_enum = postgresql.ENUM('COIN', 'BILL', name='cashtype', create_type=False)

    op.create_table(
        'cash',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('cash_type', cash_type_enum, nullable=False),
        sa.Column('cash', sa.Integer, nullable=True),
        sa.Column('stock', sa.Integer, nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.Integer, nullable=True),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('updated_by', sa.Integer, nullable=True),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('deleted_by', sa.Integer, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("cash")
    op.execute("DROP TYPE IF EXISTS cashtype;")
