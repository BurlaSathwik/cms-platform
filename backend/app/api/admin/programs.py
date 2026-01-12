from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from uuid import UUID
from datetime import datetime

from app.core.rbac import require_editor, require_viewer
from app.db.session import get_db
from app.models.program import Program, ProgramStatus
from app.models.lesson import LessonStatus
from app.models.user import UserRole
from app.schemas.program import ProgramCreate, ProgramDetailOut
from app.core.deps import get_current_role

router = APIRouter()

@router.get(
    "/",
    response_model=list[ProgramDetailOut],
    dependencies=[Depends(require_viewer)],
)
def list_programs(db: Session = Depends(get_db)):
    return (
        db.query(Program)
        .options(selectinload(Program.assets))
        .order_by(Program.created_at.desc())
        .all()
    )

@router.get(
    "/{program_id}",
    response_model=ProgramDetailOut,
    dependencies=[Depends(require_viewer)],
)
def get_program(
    program_id: UUID,
    db: Session = Depends(get_db),
    role: UserRole = Depends(get_current_role),
):
    program = (
        db.query(Program)
        .options(selectinload(Program.assets))
        .filter(Program.id == program_id)
        .first()
    )

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    if role == UserRole.viewer:
        for term in program.terms:
            term.lessons = [
                l for l in term.lessons
                if l.status == LessonStatus.published
            ]

    return program
@router.post(
    "/",
    response_model=ProgramDetailOut,
    dependencies=[Depends(require_editor)],
)
def create_program(
    data: ProgramCreate,
    db: Session = Depends(get_db),
):
    # validation: primary language must be included
    if data.language_primary not in data.languages_available:
        raise HTTPException(
            status_code=400,
            detail="languages_available must include language_primary",
        )

    program = Program(**data.dict())
    db.add(program)
    db.commit()
    db.refresh(program)

    return program
