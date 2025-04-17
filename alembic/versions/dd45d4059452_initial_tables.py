"""Initial tables

Revision ID: dd45d4059452
Revises: 06d7e24d2abd
Create Date: 2025-04-16 23:20:50.823277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd45d4059452'
down_revision: Union[str, None] = '06d7e24d2abd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    # Add this context for SQLite compatibility
    with op.batch_alter_table("orders") as batch_op:
        pass

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("orders") as batch_op:
        pass