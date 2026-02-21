# Copyright (c) 2026 Any1Key
"""user settings

Revision ID: 0002_user_settings
Revises: 0001_initial
Create Date: 2026-02-21
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_user_settings"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_settings",
        sa.Column("user_id", sa.BigInteger(), primary_key=True),
        sa.Column("lang", sa.String(length=8), nullable=False, server_default="ru"),
    )


def downgrade() -> None:
    op.drop_table("user_settings")
