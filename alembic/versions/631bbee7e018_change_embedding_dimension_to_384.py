"""change embedding dimension to 384

Revision ID: 631bbee7e018
Revises: a2ad10c30a4d
Create Date: 2026-08-28 15:56:08.265263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '631bbee7e018'
down_revision: Union[str, Sequence[str], None] = 'a2ad10c30a4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.drop_column(
        "chunks",
        "embedding",
    )

    op.add_column(
        "chunks",
        sa.Column(
            "embedding",
            pgvector.sqlalchemy.Vector(384),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:

    op.drop_column(
        "chunks",
        "embedding",
    )

    op.add_column(
        "chunks",
        sa.Column(
            "embedding",
            pgvector.sqlalchemy.Vector(1536),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
