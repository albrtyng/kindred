"""Initial schema.

Revision ID: 20260714_01
Revises:
Create Date: 2026-07-14 00:00:00

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "20260714_01"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
