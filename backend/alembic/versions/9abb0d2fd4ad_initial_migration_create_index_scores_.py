"""Initial migration: create index_scores and media_articles tables

Revision ID: 9abb0d2fd4ad
Revises: 
Create Date: 2025-11-15 13:57:24.615743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9abb0d2fd4ad'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Note: SQLite ne supporte pas ALTER COLUMN pour changer le type
    # Les colonnes content et image_url existent déjà en TEXT dans la DB
    # Cette migration est une no-op pour marquer l'état actuel
    # Pour SQLite, TEXT et String() sont équivalents
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # Note: SQLite ne supporte pas ALTER COLUMN
    # Cette migration est une no-op
    pass
