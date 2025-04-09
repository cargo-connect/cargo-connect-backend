"""Add item_category to orders

Revision ID: 5ce67f004ea9
Revises: 760a434432f7
Create Date: 2025-04-09 02:39:08.173259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '5ce67f004ea9'
down_revision: Union[str, None] = '760a434432f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    item_category_enum = postgresql.ENUM(
        'documents', 'food', 'clothings', 'electronics', 'gifts', 'beauty', 'accessories',
        name='itemcategory'
    )
    item_category_enum.create(op.get_bind()) # Create ENUM type in DB

    # Step 1: Add column as nullable
    op.add_column('orders', sa.Column(
        'item_category',
        sa.Enum('documents', 'food', 'clothings', 'electronics', 'gifts', 'beauty', 'accessories', name='itemcategory'),
        nullable=True  # allow NULLs initially
    ))

    # Step 2: Populate it with a default value (adjust as you see fit)
    op.execute("UPDATE orders SET item_category = 'documents'")

    # Step 3: Alter the column to be non-nullable
    op.alter_column('orders', 'item_category', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('orders', 'item_category')
    # Drop the ENUM type from the database
    item_category_enum = postgresql.ENUM(
        'documents', 'food', 'clothings', 'electronics', 'gifts', 'beauty', 'accessories',
        name='itemcategory'
    )
    item_category_enum.drop(op.get_bind())
