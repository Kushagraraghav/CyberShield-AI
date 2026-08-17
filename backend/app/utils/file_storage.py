"""Secure evidence file storage utilities."""

from pathlib import Path
from uuid import UUID

from fastapi import UploadFile


BASE_STORAGE_DIR = Path("storage") / "evidence"


async def save_evidence_file(
    file: UploadFile,
    organization_id: UUID,
    evidence_id: UUID,
) -> tuple[str, int]:
    """Save an uploaded evidence file and return its path and size."""

    organization_dir = BASE_STORAGE_DIR / str(organization_id)
    organization_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(file.filename or "evidence.bin").name
    destination = organization_dir / f"{evidence_id}_{safe_name}"

    size = 0

    with destination.open("wb") as output:
        while chunk := await file.read(1024 * 1024):
            output.write(chunk)
            size += len(chunk)

    await file.close()

    return str(destination), size
