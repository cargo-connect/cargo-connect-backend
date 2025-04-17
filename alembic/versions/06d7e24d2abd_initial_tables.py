"""Initial tables

Revision ID: 06d7e24d2abd
Revises: 36bc44368573
Create Date: 2025-04-16 23:12:12.807956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06d7e24d2abd'
down_revision: Union[str, None] = '36bc44368573'
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