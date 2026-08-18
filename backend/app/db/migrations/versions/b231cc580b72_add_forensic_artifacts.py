from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b231cc580b72"
down_revision: Union[str, Sequence[str], None] = "549609f0c977"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "forensic_artifacts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("evidence_id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("artifact_type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("path", sa.String(length=1000), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("hash_value", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("discovered_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_artifact_evidence_id",
        "forensic_artifacts",
        ["evidence_id"],
        unique=False,
    )

    op.create_index(
        "idx_artifact_name",
        "forensic_artifacts",
        ["name"],
        unique=False,
    )

    op.create_index(
        "idx_artifact_organization_id",
        "forensic_artifacts",
        ["organization_id"],
        unique=False,
    )

    op.create_index(
        "idx_artifact_type",
        "forensic_artifacts",
        ["artifact_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "idx_artifact_type",
        table_name="forensic_artifacts",
    )

    op.drop_index(
        "idx_artifact_organization_id",
        table_name="forensic_artifacts",
    )

    op.drop_index(
        "idx_artifact_name",
        table_name="forensic_artifacts",
    )

    op.drop_index(
        "idx_artifact_evidence_id",
        table_name="forensic_artifacts",
    )

    op.drop_table("forensic_artifacts")
