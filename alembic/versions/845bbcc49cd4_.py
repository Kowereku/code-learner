"""empty message

Revision ID: 845bbcc49cd4
Revises: 592b46b593b0
Create Date: 2026-10-19 14:58:59.674143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '845bbcc49cd4'
down_revision: Union[str, Sequence[str], None] = '592b46b593b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
