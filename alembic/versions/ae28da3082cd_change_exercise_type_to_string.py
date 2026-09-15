"""change_exercise_type_to_string

Revision ID: ae28da3082cd
Revises: 809d50f5847a
Create Date: 2026-09-15 12:54:54.989564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae28da3082cd'
down_revision: Union[str, Sequence[str], None] = '809d50f5847a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'exercises',
        'type',
        existing_type=sa.Enum('multiple_choice', 'code', 'fill_in_blank', 'true_false', name='exercise_type'),
        type_=sa.String(length=50),
        postgresql_using='type::text',
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'exercises',
        'type',
        existing_type=sa.String(length=50),
        type_=sa.Enum('multiple_choice', 'code', 'fill_in_blank', 'true_false', name='exercise_type'),
        postgresql_using='type::exercise_type',
        nullable=False,
    )
