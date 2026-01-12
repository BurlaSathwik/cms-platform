from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.program import Program
from app.models.program_asset import ProgramAsset
from app.core.rbac import require_editor
from app.schemas.program_asset import ProgramPosterCreate  # ✅ USE IT

router = APIRouter(prefix="/{program_id}/assets")


@router.post("/", dependencies=[Depends(require_editor)])
def add_program_asset(
    program_id: UUID,
    payload: ProgramPosterCreate,
    db: Session = Depends(get_db),
):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(404, "Program not found")

    # 🔍 Check if asset already exists
    asset = (
        db.query(ProgramAsset)
        .filter(
            ProgramAsset.program_id == program_id,
            ProgramAsset.language == payload.language,
            ProgramAsset.variant == payload.variant,
        )
        .first()
    )

    # 🔁 UPDATE if exists
    if asset:
        asset.url = payload.url
    else:
        asset = ProgramAsset(
            program_id=program_id,
            language=payload.language,
            variant=payload.variant,
            url=payload.url,
        )
        db.add(asset)

    db.commit()
    db.refresh(asset)
    return asset

