"""add threat intelligence feeds

Revision ID: 8d940f5be496
Revises: a1877db340e3
Create Date: 2026-08-17 20:44:25.828923
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8d940f5be496"
down_revision: Union[str, Sequence[str], None] = "a1877db340e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create threat intelligence feeds table."""

    op.create_table(
        "threat_intelligence_feeds",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("feed_type", sa.String(length=50), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("feed_url", sa.String(length=1000), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "last_fetched_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "last_successful_fetch_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_threat_feed_is_active",
        "threat_intelligence_feeds",
        ["is_active"],
        unique=False,
    )

    op.create_index(
        "idx_threat_feed_organization_id",
        "threat_intelligence_feeds",
        ["organization_id"],
        unique=False,
    )

    op.create_index(
        "idx_threat_feed_type",
        "threat_intelligence_feeds",
        ["feed_type"],
        unique=False,
    )


def downgrade() -> None:
    """Drop threat intelligence feeds table."""

    op.drop_index(
        "idx_threat_feed_type",
        table_name="threat_intelligence_feeds",
    )

    op.drop_index(
        "idx_threat_feed_organization_id",
        table_name="threat_intelligence_feeds",
    )

    op.drop_index(
        "idx_threat_feed_is_active",
        table_name="threat_intelligence_feeds",
    )

    op.drop_table("threat_intelligence_feeds")
