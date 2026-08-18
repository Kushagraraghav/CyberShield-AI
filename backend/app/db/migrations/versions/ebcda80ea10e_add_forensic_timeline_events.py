"""add forensic timeline events

Revision ID: ebcda80ea10e
Revises: b231cc580b72
Create Date: 2026-08-18 23:03:47.567035
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ebcda80ea10e"
down_revision: Union[str, Sequence[str], None] = "b231cc580b72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "forensic_timeline_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("evidence_id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("artifact_id", sa.Uuid(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["forensic_artifacts.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["cases.id"],
            ondelete="CASCADE",
        ),
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
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_timeline_case_id",
        "forensic_timeline_events",
        ["case_id"],
        unique=False,
    )
    op.create_index(
        "idx_timeline_evidence_id",
        "forensic_timeline_events",
        ["evidence_id"],
        unique=False,
    )
    op.create_index(
        "idx_timeline_organization_id",
        "forensic_timeline_events",
        ["organization_id"],
        unique=False,
    )
    op.create_index(
        "idx_timeline_event_time",
        "forensic_timeline_events",
        ["event_time"],
        unique=False,
    )
    op.create_index(
        "idx_timeline_event_type",
        "forensic_timeline_events",
        ["event_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "idx_timeline_event_type",
        table_name="forensic_timeline_events",
    )
    op.drop_index(
        "idx_timeline_event_time",
        table_name="forensic_timeline_events",
    )
    op.drop_index(
        "idx_timeline_organization_id",
        table_name="forensic_timeline_events",
    )
    op.drop_index(
        "idx_timeline_evidence_id",
        table_name="forensic_timeline_events",
    )
    op.drop_index(
        "idx_timeline_case_id",
        table_name="forensic_timeline_events",
    )
    op.drop_table("forensic_timeline_events")