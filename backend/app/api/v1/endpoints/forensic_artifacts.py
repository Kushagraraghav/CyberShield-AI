from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.forensic_artifact import (
    ForensicArtifactCreate,
    ForensicArtifactOut,
    ForensicArtifactUpdate,
)
from app.services.forensic_artifact_service import ForensicArtifactService
from app.api.v1.dependencies import require_evidence_analyst, require_evidence_viewer
from app.models.user import User


router = APIRouter(
    prefix="/forensic-artifacts",
    tags=["Forensic Artifacts"],
)


@router.post(
    "",
    response_model=ForensicArtifactOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_artifact(
    payload: ForensicArtifactCreate,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_analyst),
    db: AsyncSession = Depends(get_db),
):
    return await ForensicArtifactService.create_artifact(
        db=db,
        evidence_id=payload.evidence_id,
        organization_id=organization_id,
        artifact_type=payload.artifact_type,
        name=payload.name,
        path=payload.path,
        description=payload.description,
        source=payload.source,
        hash_value=payload.hash_value,
        status=payload.status,
        discovered_at=payload.discovered_at,
    )


@router.get(
    "/{artifact_id}",
    response_model=ForensicArtifactOut,
)
async def get_artifact(
    artifact_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_viewer),
    db: AsyncSession = Depends(get_db),
):
    artifact = await ForensicArtifactService.get_artifact(
        db=db,
        artifact_id=artifact_id,
        organization_id=organization_id,
    )

    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forensic artifact not found",
        )

    return artifact


@router.get(
    "/evidence/{evidence_id}",
    response_model=list[ForensicArtifactOut],
)
async def list_evidence_artifacts(
    evidence_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_viewer),
    db: AsyncSession = Depends(get_db),
):
    return list(
        await ForensicArtifactService.list_evidence_artifacts(
            db=db,
            evidence_id=evidence_id,
            organization_id=organization_id,
        )
    )


@router.patch(
    "/{artifact_id}",
    response_model=ForensicArtifactOut,
)
async def update_artifact(
    artifact_id: UUID,
    payload: ForensicArtifactUpdate,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_analyst),
    db: AsyncSession = Depends(get_db),
):
    artifact = await ForensicArtifactService.get_artifact(
        db=db,
        artifact_id=artifact_id,
        organization_id=organization_id,
    )

    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forensic artifact not found",
        )

    return await ForensicArtifactService.update_artifact(
        db=db,
        artifact=artifact,
        artifact_type=payload.artifact_type,
        name=payload.name,
        path=payload.path,
        description=payload.description,
        source=payload.source,
        hash_value=payload.hash_value,
        status=payload.status,
        discovered_at=payload.discovered_at,
    )


@router.delete(
    "/{artifact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_artifact(
    artifact_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_analyst),
    db: AsyncSession = Depends(get_db),
):
    artifact = await ForensicArtifactService.get_artifact(
        db=db,
        artifact_id=artifact_id,
        organization_id=organization_id,
    )

    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forensic artifact not found",
        )

    await ForensicArtifactService.delete_artifact(
        db=db,
        artifact=artifact,
    )



