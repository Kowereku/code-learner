"""empty message

Revision ID: 592b46b593b0
Revises: 68bebf6f03d4, a3598b59fe19
Create Date: 2026-10-19 14:41:09.646322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '592b46b593b0'
down_revision: Union[str, Sequence[str], None] = ('68bebf6f03d4', 'a3598b59fe19')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
