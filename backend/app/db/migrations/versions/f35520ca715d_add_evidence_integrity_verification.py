"""add evidence integrity verification

Revision ID: f35520ca715d
Revises: 8d940f5be496
Create Date: 2026-08-17 23:54:58.264169

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f35520ca715d"
down_revision: Union[str, Sequence[str], None] = "8d940f5be496"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "evidence_custody",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("evidence_id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("performed_by", sa.Uuid(), nullable=True),
        sa.Column("from_holder", sa.String(length=255), nullable=True),
        sa.Column("to_holder", sa.String(length=255), nullable=True),
        sa.Column("location", sa.String(length=500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("integrity_hash", sa.String(length=64), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
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
            ["performed_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_custody_evidence_id",
        "evidence_custody",
        ["evidence_id"],
        unique=False,
    )
    op.create_index(
        "idx_custody_organization_id",
        "evidence_custody",
        ["organization_id"],
        unique=False,
    )
    op.create_index(
        "idx_custody_performed_by",
        "evidence_custody",
        ["performed_by"],
        unique=False,
    )
    op.create_index(
        "idx_custody_timestamp",
        "evidence_custody",
        ["timestamp"],
        unique=False,
    )

    op.create_table(
        "evidence_integrity_verifications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("evidence_id", sa.Uuid(), nullable=False),
        sa.Column("algorithm", sa.String(length=20), nullable=False),
        sa.Column("expected_hash", sa.String(length=128), nullable=False),
        sa.Column("calculated_hash", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("verified_by", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(
            ["evidence_id"],
            ["evidence.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["verified_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_integrity_evidence_id",
        "evidence_integrity_verifications",
        ["evidence_id"],
        unique=False,
    )
    op.create_index(
        "idx_integrity_status",
        "evidence_integrity_verifications",
        ["status"],
        unique=False,
    )
    op.create_index(
        "idx_integrity_verified_at",
        "evidence_integrity_verifications",
        ["verified_at"],
        unique=False,
    )

    # Evidence metadata support
    op.add_column(
        "evidence",
        sa.Column("metadata", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("evidence", "metadata")

    op.drop_index(
        "idx_integrity_verified_at",
        table_name="evidence_integrity_verifications",
    )
    op.drop_index(
        "idx_integrity_status",
        table_name="evidence_integrity_verifications",
    )
    op.drop_index(
        "idx_integrity_evidence_id",
        table_name="evidence_integrity_verifications",
    )
    op.drop_table("evidence_integrity_verifications")

    op.drop_index(
        "idx_custody_timestamp",
        table_name="evidence_custody",
    )
    op.drop_index(
        "idx_custody_performed_by",
        table_name="evidence_custody",
    )
    op.drop_index(
        "idx_custody_organization_id",
        table_name="evidence_custody",
    )
    op.drop_index(
        "idx_custody_evidence_id",
        table_name="evidence_custody",
    )
    op.drop_table("evidence_custody")