"""Evidence integrity verification service."""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.evidence_integrity_repository import (
    EvidenceIntegrityRepository,
)
from app.repositories.evidence_repository import EvidenceRepository
from app.schemas.evidence_integrity import (
    EvidenceIntegrityVerificationResponse,
)


class EvidenceIntegrityService:
    """Service for evidence integrity verification."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.evidence_repository = EvidenceRepository(session)
        self.integrity_repository = EvidenceIntegrityRepository(session)

    async def verify(
        self,
        evidence_id: UUID,
        algorithm: str = "sha256",
        verified_by: UUID | None = None,
    ) -> EvidenceIntegrityVerificationResponse | None:
        """Calculate and verify the hash of an evidence file."""

        evidence = await self.evidence_repository.get_by_id(evidence_id)

        if evidence is None:
            return None

        if not evidence.storage_path:
            raise ValueError(
                "Evidence does not have a storage path"
            )

        file_path = Path(evidence.storage_path)

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Evidence file not found: {evidence.storage_path}"
            )

        algorithm = algorithm.lower()

        if algorithm not in {"sha256", "md5"}:
            raise ValueError(
                "Unsupported hash algorithm. Use sha256 or md5."
            )

        expected_hash = (
            evidence.sha256_hash
            if algorithm == "sha256"
            else evidence.md5_hash
        )

        if not expected_hash:
            raise ValueError(
                f"No expected {algorithm} hash is stored for this evidence"
            )

        hash_function = hashlib.sha256 if algorithm == "sha256" else hashlib.md5

        digest = hash_function()

        with file_path.open("rb") as evidence_file:
            while chunk := evidence_file.read(1024 * 1024):
                digest.update(chunk)

        calculated_hash = digest.hexdigest()

        status = (
            "verified"
            if calculated_hash.lower() == expected_hash.lower()
            else "failed"
        )

        details = (
            f"{algorithm.upper()} hash verification successful."
            if status == "verified"
            else (
                f"{algorithm.upper()} hash mismatch. "
                f"Expected {expected_hash}, "
                f"calculated {calculated_hash}."
            )
        )

        verification = await self.integrity_repository.create(
            id=uuid4(),
            evidence_id=evidence_id,
            algorithm=algorithm,
            expected_hash=expected_hash,
            calculated_hash=calculated_hash,
            status=status,
            details=details,
            verified_at=datetime.now(timezone.utc),
            verified_by=verified_by,
        )

        return EvidenceIntegrityVerificationResponse.model_validate(
            verification
        )

    async def get_latest(
        self,
        evidence_id: UUID,
    ) -> EvidenceIntegrityVerificationResponse | None:
        """Get the latest integrity verification."""

        verification = await self.integrity_repository.get_latest_by_evidence(
            evidence_id
        )

        if verification is None:
            return None

        return EvidenceIntegrityVerificationResponse.model_validate(
            verification
        )

    async def get_history(
        self,
        evidence_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[EvidenceIntegrityVerificationResponse]:
        """Get integrity verification history."""

        verifications = await self.integrity_repository.get_by_evidence(
            evidence_id=evidence_id,
            skip=skip,
            limit=limit,
        )

        return [
            EvidenceIntegrityVerificationResponse.model_validate(
                verification
            )
            for verification in verifications
        ]
