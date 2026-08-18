"""add evidence analysis

Revision ID: 549609f0c977
Revises: f35520ca715d
Create Date: 2026-08-18 00:16:38.915002
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "549609f0c977"
down_revision: Union[str, Sequence[str], None] = "f35520ca715d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create evidence analysis table."""

    op.create_table(
        "evidence_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("evidence_id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("findings", sa.Text(), nullable=True),
        sa.Column("tool_used", sa.String(length=255), nullable=True),
        sa.Column("analyst_notes", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("analyzed_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["evidence_id"],
            ["evidence.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["analyzed_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_analysis_evidence_id",
        "evidence_analyses",
        ["evidence_id"],
        unique=False,
    )

    op.create_index(
        "idx_analysis_organization_id",
        "evidence_analyses",
        ["organization_id"],
        unique=False,
    )

    op.create_index(
        "idx_analysis_type",
        "evidence_analyses",
        ["analysis_type"],
        unique=False,
    )

    op.create_index(
        "idx_analysis_status",
        "evidence_analyses",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    """Remove evidence analysis table."""

    op.drop_index(
        "idx_analysis_status",
        table_name="evidence_analyses",
    )

    op.drop_index(
        "idx_analysis_type",
        table_name="evidence_analyses",
    )

    op.drop_index(
        "idx_analysis_organization_id",
        table_name="evidence_analyses",
    )

    op.drop_index(
        "idx_analysis_evidence_id",
        table_name="evidence_analyses",
    )

    op.drop_table("evidence_analyses")
