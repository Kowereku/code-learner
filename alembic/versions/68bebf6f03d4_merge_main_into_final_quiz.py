"""merge main into final quiz

Revision ID: 68bebf6f03d4
Revises: 5772f9874ac8, 83f343a2c723
Create Date: 2026-10-19 13:43:06.018597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68bebf6f03d4'
down_revision: Union[str, Sequence[str], None] = ('5772f9874ac8', '83f343a2c723')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
