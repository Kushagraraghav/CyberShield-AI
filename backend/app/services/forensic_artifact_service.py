from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.forensic_artifact import ForensicArtifact
from app.repositories.forensic_artifact_repository import ForensicArtifactRepository


class ForensicArtifactService:
    """Business logic for forensic artifacts."""

    @staticmethod
    async def create_artifact(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
        artifact_type: str,
        name: str,
        path: str | None = None,
        description: str | None = None,
        source: str | None = None,
        hash_value: str | None = None,
        status: str | None = None,
        discovered_at: datetime | None = None,
    ) -> ForensicArtifact:
        artifact = ForensicArtifact(
            evidence_id=evidence_id,
            organization_id=organization_id,
            artifact_type=artifact_type,
            name=name,
            path=path,
            description=description,
            source=source,
            hash_value=hash_value,
            status=status or "identified",
            discovered_at=discovered_at,
        )

        return await ForensicArtifactRepository.create(db, artifact)

    @staticmethod
    async def get_artifact(
        db: AsyncSession,
        artifact_id: UUID,
        organization_id: UUID,
    ) -> ForensicArtifact | None:
        return await ForensicArtifactRepository.get_by_id(
            db,
            artifact_id,
            organization_id,
        )

    @staticmethod
    async def list_evidence_artifacts(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
    ):
        return await ForensicArtifactRepository.list_by_evidence(
            db,
            evidence_id,
            organization_id,
        )

    @staticmethod
    async def update_artifact(
        db: AsyncSession,
        artifact: ForensicArtifact,
        artifact_type: str | None = None,
        name: str | None = None,
        path: str | None = None,
        description: str | None = None,
        source: str | None = None,
        hash_value: str | None = None,
        status: str | None = None,
        discovered_at: datetime | None = None,
    ) -> ForensicArtifact:
        if artifact_type is not None:
            artifact.artifact_type = artifact_type
        if name is not None:
            artifact.name = name
        if path is not None:
            artifact.path = path
        if description is not None:
            artifact.description = description
        if source is not None:
            artifact.source = source
        if hash_value is not None:
            artifact.hash_value = hash_value
        if status is not None:
            artifact.status = status
        if discovered_at is not None:
            artifact.discovered_at = discovered_at

        artifact.updated_at = datetime.now(timezone.utc)

        return await ForensicArtifactRepository.update(db, artifact)

    @staticmethod
    async def delete_artifact(
        db: AsyncSession,
        artifact: ForensicArtifact,
    ) -> None:
        await db.delete(artifact)
        await db.flush()
