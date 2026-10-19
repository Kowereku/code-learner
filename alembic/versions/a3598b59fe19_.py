"""empty message

Revision ID: a3598b59fe19
Revises: 012c794dc05e, 83f343a2c723
Create Date: 2026-10-19 12:51:05.633615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3598b59fe19'
down_revision: Union[str, Sequence[str], None] = ('012c794dc05e', '83f343a2c723')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
