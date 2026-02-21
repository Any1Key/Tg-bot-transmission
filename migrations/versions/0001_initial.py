# Copyright (c) 2026 Any1Key
"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2026-02-21
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "torrents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("torrent_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("torrent_name", sa.String(512), nullable=False),
        sa.Column("download_dir", sa.String(512), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("notified", sa.Boolean(), nullable=False),
        sa.Column("ratio", sa.Float(), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=True),
        sa.Column("download_seconds", sa.Integer(), nullable=True),
        sa.Column("added_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("torrents")
